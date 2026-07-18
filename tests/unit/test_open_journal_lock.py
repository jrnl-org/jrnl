# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import os

import filelock
import pytest

from jrnl.exception import JrnlException
from jrnl.journals import open_journal_with_lock
from jrnl.journals import open_journal_without_lock
from jrnl.lock import journal_lock_path


def _config(journal_path: str) -> dict:
    return {
        "journal": journal_path,
        "journals": {"default": journal_path},
        "encrypt": False,
        "default_hour": 9,
        "default_minute": 0,
        "timeformat": "%Y-%m-%d %H:%M",
        "tagsymbols": "@",
        "highlight": True,
        "linewrap": 80,
        "indent_character": "|",
    }


def test_open_journal_acquires_lock_and_release_lock_frees_it(tmp_path):
    journal_path = str(tmp_path / "journal.txt")
    config = _config(journal_path)

    journal = open_journal_with_lock("default", config)
    try:
        assert journal._lock is not None
        assert journal._lock.is_locked
    finally:
        journal.release_lock()

    assert journal._lock is None
    # the lock file is intentionally left in place after release (see
    # release_journal_lock's docstring) to avoid an unlink race with a
    # waiting process
    assert os.path.exists(journal_lock_path(journal_path))


def test_open_journal_as_context_manager_releases_lock_on_exit(tmp_path):
    journal_path = str(tmp_path / "journal.txt")
    config = _config(journal_path)

    with open_journal_with_lock("default", config) as journal:
        assert journal._lock is not None
        assert journal._lock.is_locked

    assert journal._lock is None


def test_open_journal_as_context_manager_releases_lock_on_exception(tmp_path):
    journal_path = str(tmp_path / "journal.txt")
    config = _config(journal_path)

    with pytest.raises(ValueError):
        with open_journal_with_lock("default", config) as journal:
            msg = "boom"
            raise ValueError(msg)

    assert journal._lock is None


def test_open_journal_raises_when_another_process_holds_the_lock(tmp_path):
    journal_path = str(tmp_path / "journal.txt")
    config = _config(journal_path)

    blocking_lock = filelock.FileLock(journal_lock_path(journal_path))
    blocking_lock.acquire()
    try:
        with pytest.raises(JrnlException) as exc_info:
            open_journal_with_lock("default", config)
        assert exc_info.value.messages[0].params["journal_name"] == "default"
    finally:
        blocking_lock.release()


def test_open_journal_does_not_acquire_a_lock(tmp_path):
    journal_path = str(tmp_path / "journal.txt")
    config = _config(journal_path)

    with open_journal_without_lock("default", config) as journal:
        assert journal._lock is None
    assert not os.path.exists(journal_lock_path(journal_path))


def test_open_journal_succeeds_while_open_journal_with_lock_holds_the_lock(tmp_path):
    journal_path = str(tmp_path / "journal.txt")
    config = _config(journal_path)

    with open_journal_with_lock("default", config):
        # a read-only open shouldn't be blocked by a concurrent writer
        with open_journal_without_lock("default", config) as reader:
            assert reader._lock is None


def test_open_and_write_journal_works_normally_single_process(tmp_path):
    journal_path = str(tmp_path / "journal.txt")
    config = _config(journal_path)

    with open_journal_with_lock("default", config) as journal:
        journal.new_entry("test entry")
        journal.write()

    with open_journal_with_lock("default", config) as reopened:
        assert len(reopened) == 1
        assert "test entry" in reopened.entries[0].text
