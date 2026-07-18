# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import os
import subprocess
import sys
from unittest.mock import patch

import filelock
import pytest

from jrnl.exception import JrnlException
from jrnl.lock import acquire_journal_lock
from jrnl.lock import journal_lock_path
from jrnl.lock import release_journal_lock
from jrnl.messages import MsgText


def _spawn_lock_holder(journal_path: str) -> subprocess.Popen:
    """Spawns a real subprocess that acquires the lock for journal_path and
    holds it, so tests can exercise killing an actual killable PID."""
    script = "\n".join(
        [
            "import time",
            "from jrnl.lock import acquire_journal_lock",
            # must keep a reference: filelock's __del__ releases on GC
            f"lock = acquire_journal_lock({journal_path!r}, 'default')",
            "print('locked', flush=True)",
            "time.sleep(30)",
        ]
    )
    proc = subprocess.Popen(
        [sys.executable, "-c", script], stdout=subprocess.PIPE, text=True
    )
    proc.stdout.readline()  # wait for the child to confirm it holds the lock
    return proc


def test_journal_lock_path_is_not_a_sibling_of_the_journal(tmp_path):
    # Lock files are never deleted (see release_journal_lock), so they live
    # in a shared lock directory instead of next to the journal, which may
    # be a git repo, a synced folder, etc.
    journal_path = str(tmp_path / "journal.txt")
    lock_path = journal_lock_path(journal_path)
    assert os.path.dirname(lock_path) != os.path.dirname(journal_path)


def test_journal_lock_path_is_stable_for_the_same_journal(tmp_path):
    journal_path = str(tmp_path / "journal.txt")
    assert journal_lock_path(journal_path) == journal_lock_path(journal_path)


def test_journal_lock_path_differs_between_journals(tmp_path):
    assert journal_lock_path(str(tmp_path / "a.txt")) != journal_lock_path(
        str(tmp_path / "b.txt")
    )


def test_journal_lock_path_ignores_trailing_separator(tmp_path):
    # Folder/DayOne journals are directories; a trailing separator shouldn't
    # change the journal's identity for locking purposes.
    journal_dir = str(tmp_path / "myjournal")
    assert journal_lock_path(journal_dir) == journal_lock_path(journal_dir + os.sep)


def test_journal_lock_path_is_stable_across_equivalent_path_spellings(tmp_path):
    # The same journal should map to the same lock file regardless of the
    # exact (but equivalent) string used to refer to it.
    journal_dir = tmp_path / "myjournal"
    journal_dir.mkdir()
    equivalent_path = tmp_path / "." / "myjournal"
    assert journal_lock_path(str(journal_dir)) == journal_lock_path(
        str(equivalent_path)
    )


@pytest.mark.parametrize(
    "exception",
    [
        OSError,  # Python 3.13+ explicitly wraps "no username found" as this
        ImportError,  # Windows has no 'pwd' module; older getpass lets
        # `import pwd` inside getuser()'s fallback raise this raw when no
        # LOGNAME/USER/LNAME/USERNAME env var is set either (observed in CI:
        # https://github.com/jrnl-org/jrnl/actions/runs/29493115956)
    ],
)
def test_journal_lock_path_falls_back_when_no_username_is_set(tmp_path, exception):
    journal_path = str(tmp_path / "journal.txt")
    with patch("jrnl.lock.getpass.getuser", side_effect=exception):
        lock_path = journal_lock_path(journal_path)
    assert os.path.exists(os.path.dirname(lock_path))


def test_acquire_and_release_round_trip(tmp_path):
    journal_path = str(tmp_path / "journal.txt")

    lock = acquire_journal_lock(journal_path, "default")
    assert lock.is_locked

    lock_path = journal_lock_path(journal_path)
    assert os.path.exists(lock_path)

    release_journal_lock(lock)
    assert not lock.is_locked
    # The lock file is intentionally left in place after release: deleting it
    # here would race with a waiting process that opens+locks it the instant
    # we release, letting a third process create a fresh inode afterwards and
    # hold an independent, non-conflicting lock on the same path.
    assert os.path.exists(lock_path)


def test_acquire_raises_when_already_locked(tmp_path):
    journal_path = str(tmp_path / "journal.txt")
    lock_path = journal_lock_path(journal_path)

    other_process_lock = filelock.FileLock(lock_path)
    other_process_lock.acquire()
    try:
        with pytest.raises(JrnlException) as exc_info:
            acquire_journal_lock(journal_path, "default")

        message = exc_info.value.messages[0]
        assert message.params["journal_name"] == "default"
        # the other process's flock is held via a bare filelock.FileLock,
        # which never writes a PID into the file, so this falls back to
        # "unknown process" rather than raising while formatting the message
        assert message.params["process"] == "unknown process"
    finally:
        other_process_lock.release()


# Windows can't delete a file while a handle to it is still open (no
# FILE_SHARE_DELETE), so this scenario can't be set up there.
@pytest.mark.skip_win
def test_release_does_not_raise_if_lock_file_already_removed_externally(tmp_path):
    journal_path = str(tmp_path / "journal.txt")
    lock = acquire_journal_lock(journal_path, "default")

    os.remove(journal_lock_path(journal_path))

    # should not raise even though something else already deleted the file
    release_journal_lock(lock)


def test_acquire_does_not_prompt_when_holder_pid_is_unknown(tmp_path):
    journal_path = str(tmp_path / "journal.txt")
    lock_path = journal_lock_path(journal_path)

    # a bare filelock.FileLock never writes a PID, so there's nothing we
    # could offer to kill
    other_process_lock = filelock.FileLock(lock_path)
    other_process_lock.acquire()
    try:
        with patch("jrnl.lock.yesno") as mock_yesno:
            with pytest.raises(JrnlException):
                acquire_journal_lock(journal_path, "default")
            mock_yesno.assert_not_called()
    finally:
        other_process_lock.release()


def test_acquire_raises_when_user_declines_to_kill(tmp_path, monkeypatch):
    monkeypatch.setattr("jrnl.lock.LOCK_TIMEOUT_SECONDS", 0.3)
    journal_path = str(tmp_path / "journal.txt")

    holder = _spawn_lock_holder(journal_path)
    try:
        with patch("jrnl.lock.yesno", return_value=False):
            with pytest.raises(JrnlException) as exc_info:
                acquire_journal_lock(journal_path, "default")
            assert exc_info.value.messages[0].text == MsgText.JournalKillDeclined

        # declined to kill -- holder should still be alive
        assert holder.poll() is None
    finally:
        holder.kill()
        holder.wait()


def test_acquire_raises_distinct_message_when_kill_attempt_fails(tmp_path, monkeypatch):
    # e.g. psutil.AccessDenied trying to kill another user's process -- this
    # must not be reported as "declined" (JournalKillDeclined), since the
    # user *did* say yes; we just couldn't follow through.
    monkeypatch.setattr("jrnl.lock.LOCK_TIMEOUT_SECONDS", 0.3)
    journal_path = str(tmp_path / "journal.txt")

    holder = _spawn_lock_holder(journal_path)
    try:
        with (
            patch("jrnl.lock.yesno", return_value=True),
            patch("jrnl.lock._kill_and_wait", return_value=False),
        ):
            with pytest.raises(JrnlException) as exc_info:
                acquire_journal_lock(journal_path, "default")
            assert exc_info.value.messages[0].text == MsgText.JournalKillFailed

        # _kill_and_wait was mocked out, so the holder was never touched
        assert holder.poll() is None
    finally:
        holder.kill()
        holder.wait()


def test_acquire_offers_to_kill_and_retries_when_user_confirms(tmp_path, monkeypatch):
    monkeypatch.setattr("jrnl.lock.LOCK_TIMEOUT_SECONDS", 0.3)
    journal_path = str(tmp_path / "journal.txt")

    holder = _spawn_lock_holder(journal_path)
    try:
        with patch("jrnl.lock.yesno", return_value=True):
            lock = acquire_journal_lock(journal_path, "default")

        assert lock.is_locked
        # Popen.wait() raises TimeoutExpired if the process is still alive
        # after 5s, which would fail this test; returning normally is the
        # actual "confirmed dead" check (it never returns None).
        holder.wait(timeout=5)
        release_journal_lock(lock)
    finally:
        if holder.poll() is None:
            holder.kill()
            holder.wait()
