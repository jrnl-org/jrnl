# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import json
import shutil
import subprocess

from keyring import backend
from keyring import errors

OP_EXECUTABLE = "op"


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [OP_EXECUTABLE, *args],
        capture_output=True,
        text=True,
    )


def _item_title(service: str, username: str) -> str:
    return f"{service}/{username}"


def _ensure_authenticated() -> None:
    if _run("whoami").returncode != 0:
        msg = (
            "1Password CLI is not signed in. Run 'op signin', or enable the "
            "1Password desktop app's 'Integrate with 1Password CLI' setting, "
            "then try again."
        )
        raise RuntimeError(msg)


def _item_exists(title: str) -> bool:
    return _run("item", "get", title, "--format", "json").returncode == 0


class OnePasswordBackend(backend.KeyringBackend):
    """A keyring backend that stores secrets as Login items in 1Password,
    via the 'op' CLI. Each (service, username) pair maps to one item,
    titled '{service}/{username}', so distinct callers never collide on a
    single item. Only the password field is populated -- the item's
    username field is left blank, since the (service, username) pair is
    already captured in the title.

    Unlike the OS-native backends, priority is not used for automatic
    discovery here -- callers must opt in explicitly via
    keyring.set_keyring(OnePasswordBackend()) rather than relying on
    keyring's own priority-based backend selection. This avoids ties with
    other backends (see jrnl's own commit history for why).
    """

    priority = 1

    @classmethod
    def is_available(cls) -> bool:
        return shutil.which(OP_EXECUTABLE) is not None

    def item_exists(self, service: str, username: str) -> bool:
        """Whether an item already exists for this (service, username) pair,
        i.e. whether set_password() would edit an existing item rather than
        create a new one."""
        _ensure_authenticated()
        return _item_exists(_item_title(service, username))

    def get_password(self, service: str, username: str) -> str | None:
        _ensure_authenticated()
        title = _item_title(service, username)

        result = _run(
            "item",
            "get",
            title,
            "--fields",
            "label=password",
            "--reveal",
            "--format",
            "json",
        )
        if result.returncode != 0:
            return None

        try:
            parsed = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            msg = f"Unexpected response from 1Password CLI for '{title}': {e}"
            raise RuntimeError(msg) from e

        # 'op item get' returns a single field object (not a list) when only
        # one --fields value is requested, but a list of field objects when
        # multiple are requested. Normalize to a list either way.
        if isinstance(parsed, dict):
            parsed = [parsed]

        try:
            return next(f["value"] for f in parsed if f.get("label") == "password")
        except (KeyError, StopIteration, TypeError) as e:
            msg = f"Unexpected response from 1Password CLI for '{title}': {e}"
            raise RuntimeError(msg) from e

    def set_password(self, service: str, username: str, password: str) -> None:
        _ensure_authenticated()
        title = _item_title(service, username)

        if _item_exists(title):
            result = _run("item", "edit", title, f"password={password}")
        else:
            result = _run(
                "item",
                "create",
                "--category=login",
                f"--title={title}",
                f"password={password}",
            )

        if result.returncode != 0:
            msg = (
                f"1Password CLI failed to store password for '{title}': "
                f"{result.stderr.strip()}"
            )
            raise RuntimeError(msg)

    def delete_password(self, service: str, username: str) -> None:
        _ensure_authenticated()
        title = _item_title(service, username)

        if not _item_exists(title):
            raise errors.PasswordDeleteError(title)

        result = _run("item", "delete", title)
        if result.returncode != 0:
            msg = f"1Password CLI failed to delete '{title}': {result.stderr.strip()}"
            raise RuntimeError(msg)
