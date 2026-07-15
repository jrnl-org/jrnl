# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging

import keyring

from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg

SERVICE_NAME = "jrnl"


def _backend_name() -> str:
    try:
        return type(keyring.get_keyring()).__name__
    except Exception:
        return "unknown"


def _select_backend(config: dict | None) -> None:
    """Explicitly pin the active keyring backend if the config requests one,
    rather than relying on keyring's own priority-based auto-discovery.

    This is only ever opt-in: with no keyring_backend set, jrnl behaves
    exactly as before, deferring entirely to keyring's own backend
    selection.
    """
    backend_name = (config or {}).get("keyring_backend")
    if not backend_name:
        return

    if backend_name == "onepassword":
        from jrnl.encryption.OnePasswordBackend import OnePasswordBackend

        if not OnePasswordBackend.is_available():
            logging.debug(
                "Keyring: keyring_backend='onepassword' but the 'op' CLI "
                "was not found"
            )
            print_msg(Message(MsgText.OnePasswordCliNotFound, MsgStyle.WARNING))
            return

        keyring.set_keyring(OnePasswordBackend())
        return

    logging.debug("Keyring: unrecognized keyring_backend '%s'", backend_name)


def _confirm_onepassword_overwrite(
    config: dict | None, journal_name: str, keyring_key: str
) -> bool:
    """If storing to 1Password would overwrite an existing item, ask the
    user to confirm first. Returns False if the caller should abort the
    store instead."""
    if (config or {}).get("keyring_backend") != "onepassword":
        return True

    from jrnl.encryption.OnePasswordBackend import OnePasswordBackend
    from jrnl.prompt import yesno

    try:
        exists = OnePasswordBackend().item_exists(SERVICE_NAME, journal_name)
    except Exception as e:
        logging.debug(
            "Keyring (%s): could not check for an existing 1Password item: %s",
            keyring_key,
            e,
        )
        return True

    if not exists:
        return True

    return yesno(
        Message(
            MsgText.OnePasswordItemWillBeOverwritten,
            params={"journal_name": journal_name, "keyring_key": keyring_key},
        ),
        default=False,
    )


def get_keyring_password(
    journal_name: str = "default", config: dict | None = None
) -> str | None:
    _select_backend(config)
    keyring_key = f"{SERVICE_NAME}/{journal_name}"
    try:
        password = keyring.get_password(SERVICE_NAME, journal_name)
    except keyring.errors.NoKeyringError:
        logging.debug("Keyring (%s): no backend available", keyring_key)
        return None
    except Exception as e:
        # Some third-party backends don't raise keyring.errors.KeyringError
        # on failure, so this is intentionally broad.
        backend = _backend_name()
        logging.debug(
            "Keyring (%s) via %s: failed to retrieve password: %s",
            keyring_key,
            backend,
            e,
        )
        print_msg(
            Message(
                MsgText.KeyringRetrievalFailure,
                MsgStyle.ERROR,
                params={
                    "journal_name": journal_name,
                    "backend": backend,
                    "reason": str(e),
                },
            )
        )
        return None

    backend = _backend_name()
    logging.debug(
        "Keyring (%s) via %s: retrieval %s",
        keyring_key,
        backend,
        "succeeded" if password else "returned no password",
    )
    if password:
        print_msg(
            Message(
                MsgText.PasswordRetrievedFromKeyring,
                MsgStyle.NORMAL,
                params={
                    "journal_name": journal_name,
                    "backend": backend,
                    "keyring_key": keyring_key,
                },
            )
        )
    return password


def set_keyring_password(
    password: str, journal_name: str = "default", config: dict | None = None
) -> None:
    _select_backend(config)
    keyring_key = f"{SERVICE_NAME}/{journal_name}"

    if not _confirm_onepassword_overwrite(config, journal_name, keyring_key):
        print_msg(
            Message(
                MsgText.KeyringStoreCancelled,
                MsgStyle.WARNING,
                params={"journal_name": journal_name},
            )
        )
        return

    try:
        keyring.set_password(SERVICE_NAME, journal_name, password)
    except keyring.errors.NoKeyringError:
        logging.debug("Keyring (%s): no backend available", keyring_key)
        print_msg(Message(MsgText.KeyringBackendNotFound, MsgStyle.WARNING))
        return
    except Exception as e:
        # Some third-party backends don't raise keyring.errors.KeyringError
        # on failure, so this is intentionally broad.
        backend = _backend_name()
        logging.debug(
            "Keyring (%s) via %s: failed to store password: %s",
            keyring_key,
            backend,
            e,
        )
        print_msg(
            Message(
                MsgText.KeyringStorageFailure,
                MsgStyle.ERROR,
                params={
                    "journal_name": journal_name,
                    "backend": backend,
                    "reason": str(e),
                },
            )
        )
        return

    backend = _backend_name()
    logging.debug(
        "Keyring (%s) via %s: password stored successfully",
        keyring_key,
        backend,
    )
    print_msg(
        Message(
            MsgText.PasswordStoredInKeyring,
            MsgStyle.NORMAL,
            params={
                "journal_name": journal_name,
                "backend": backend,
                "keyring_key": keyring_key,
            },
        )
    )
