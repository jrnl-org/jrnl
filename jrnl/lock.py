# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import contextlib
import getpass
import hashlib
import os
import stat
import tempfile

import filelock
import psutil

from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.os_compat import on_windows
from jrnl.output import print_msg
from jrnl.prompt import yesno

# How long to wait for another jrnl process to release the journal before
# failing fast, rather than hanging indefinitely. Overridable via
# JRNL_LOCK_TIMEOUT.
LOCK_TIMEOUT_SECONDS = float(os.getenv("JRNL_LOCK_TIMEOUT", "2"))

UNKNOWN_PID = "unknown"


def _lock_owner_id() -> str:
    """Filesystem-safe identifier for the current user, used to scope the
    lock directory. Falls back to a fixed name if no username is available
    (e.g. some CI/container setups). getpass.getuser() raises OSError when
    it explicitly detects no username (Python 3.13+); on platforms without
    a 'pwd' module (Windows) and no LOGNAME/USER/LNAME/USERNAME env vars,
    older behavior lets the ImportError from `import pwd` propagate raw."""
    try:
        return getpass.getuser()
    except (OSError, ImportError):
        return "unknown"


def _lock_dir() -> str:
    """Private, per-user directory for jrnl's lock files, kept separate from
    the journal itself since lock files are never deleted (see
    release_journal_lock)."""
    lock_dir = os.path.join(tempfile.gettempdir(), f"jrnl-locks-{_lock_owner_id()}")

    with contextlib.suppress(FileNotFoundError):
        # Don't follow a symlink planted here by another local user.
        if stat.S_ISLNK(os.lstat(lock_dir).st_mode):
            os.unlink(lock_dir)

    os.makedirs(lock_dir, exist_ok=True)
    with contextlib.suppress(OSError):
        os.chmod(lock_dir, 0o700)

    return lock_dir


def journal_lock_path(journal_path: str) -> str:
    """Path to the lock file for a given journal, stored in a shared
    per-user lock directory. Keyed by the journal's canonical path, so the
    same journal always maps to the same lock file."""
    canonical = os.path.realpath(journal_path.rstrip(os.sep))
    digest = hashlib.sha256(canonical.encode()).hexdigest()[:16]
    return os.path.join(_lock_dir(), f"{digest}.lock")


# filelock's Windows backend takes a mandatory OS lock on exactly 1 byte at
# offset 0 of the lock file to represent ownership (LockFileEx, unlike
# POSIX flock which locks the whole file only against other flock callers).
# Reading or writing that byte from any other handle -- even our own, via a
# second open() -- raises a sharing violation while the lock is held. Keep
# our bookkeeping strictly past it so a contending process can still read
# who's holding the lock.
_PID_OFFSET = 1


def _read_lock_pid(lock_path: str) -> str:
    """Best-effort read of the PID left behind by the current (or last) lock
    holder. Safe to store in the lock file itself: filelock (>=3.30.0) only
    lets the actual holder write to it, never a losing contender."""
    with contextlib.suppress(OSError, ValueError):
        with open(lock_path, "rb") as f:
            f.seek(_PID_OFFSET)
            content = f.read().decode().strip()
        if content:
            int(content)  # validate it actually looks like a pid
            return content
    return UNKNOWN_PID


def _write_lock_pid(lock_path: str) -> None:
    with contextlib.suppress(OSError):
        with open(lock_path, "r+b") as f:
            f.seek(_PID_OFFSET)
            f.write(str(os.getpid()).encode())
            f.truncate()


def _process_cmdline(pid: str) -> str | None:
    """Best-effort lookup of the command line of the process holding the
    lock, to make the "journal is locked" error more actionable."""
    try:
        cmdline = psutil.Process(int(pid)).cmdline()
    except (psutil.Error, ValueError):
        return None
    return " ".join(cmdline) or None


def _kill_command(pid: str) -> str:
    if on_windows():
        return f"taskkill /F /PID {pid}"
    return f"kill -9 {pid}"


def _describe_lock_holder(lock_path: str) -> tuple[str, str]:
    """Returns a description of the current lock holder, and a "how to
    recover if it's hung" hint (empty if the holder's PID is unknown)."""
    pid = _read_lock_pid(lock_path)
    if pid == UNKNOWN_PID:
        return "unknown process", ""

    cmdline = _process_cmdline(pid)
    description = f"PID {pid}: {cmdline}" if cmdline else f"PID {pid}"
    kill_hint = (
        "\n\nIf the process is hung and needs to be killed, run:\n\n"
        f"    {_kill_command(pid)}"
    )
    return description, kill_hint


def _kill_and_wait(pid: str) -> bool:
    """Kills the given PID and waits for it to exit. Returns whether it's
    confirmed gone."""
    try:
        proc = psutil.Process(int(pid))
        proc.kill()
        proc.wait(timeout=LOCK_TIMEOUT_SECONDS)
    except psutil.NoSuchProcess:
        pass
    except (psutil.Error, ValueError):
        return False
    return True


def _still_locked_exception(
    journal_name: str, description: str, kill_hint: str
) -> JrnlException:
    return JrnlException(
        Message(
            MsgText.JournalStillLocked,
            MsgStyle.ERROR,
            {
                "journal_name": journal_name,
                "process": description,
                "kill_hint": kill_hint,
            },
        )
    )


def _handle_lock_timeout(
    lock: filelock.FileLock, lock_path: str, journal_name: str
) -> None:
    """Called when acquiring lock_path timed out. Offers to kill the holder
    and retry (default: no); raises JrnlException either way if we still
    don't hold the lock afterwards."""
    pid = _read_lock_pid(lock_path)
    description, kill_hint = _describe_lock_holder(lock_path)

    if pid == UNKNOWN_PID:
        raise _still_locked_exception(journal_name, description, kill_hint)

    print_msg(
        Message(
            MsgText.JournalLockedWarning,
            MsgStyle.WARNING,
            {"journal_name": journal_name, "process": description},
        )
    )
    should_kill = yesno(Message(MsgText.KillLockingProcessQuestion), default=False)

    if not should_kill:
        # declined -- already saw the full detail above, no need to repeat it
        raise JrnlException(Message(MsgText.JournalKillDeclined, MsgStyle.ERROR))

    if not _kill_and_wait(pid):
        raise JrnlException(
            Message(MsgText.JournalKillFailed, MsgStyle.ERROR, {"pid": pid})
        )

    try:
        lock.acquire()
        return
    except filelock.Timeout:
        # someone else grabbed it in the gap -- show who, in full
        description, kill_hint = _describe_lock_holder(lock_path)
        raise _still_locked_exception(journal_name, description, kill_hint)


def acquire_journal_lock(journal_path: str, journal_name: str) -> filelock.FileLock:
    """Acquires an exclusive lock for the given journal path. If another
    process already holds it, offers to kill it and retry (default: no)
    before raising a JrnlException."""
    lock_path = journal_lock_path(journal_path)

    # preserve_lock_file=True: without it, filelock deletes the lock file on
    # release on Windows (Unix already leaves it), and silently falls back to
    # SoftFileLock -- which also deletes on release -- if flock isn't
    # supported. Both would reintroduce the unlink race release_journal_lock
    # exists to avoid, and would wipe the PID we write into the file below.
    lock = filelock.FileLock(
        lock_path, timeout=LOCK_TIMEOUT_SECONDS, preserve_lock_file=True
    )
    try:
        lock.acquire()
    except filelock.Timeout:
        _handle_lock_timeout(lock, lock_path, journal_name)

    _write_lock_pid(lock_path)
    return lock


def release_journal_lock(lock: filelock.FileLock) -> None:
    """Releases a lock acquired by acquire_journal_lock.

    Does NOT delete the on-disk lock file -- unlinking it here could race
    with a waiting process and let two processes hold the lock at once.
    preserve_lock_file=True (set in acquire_journal_lock) makes filelock
    enforce that too.
    """
    lock.release()
