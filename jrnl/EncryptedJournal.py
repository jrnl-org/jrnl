# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import base64
import hashlib
import logging
import os
from typing import Callable
from typing import Optional

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from jrnl.exception import JrnlException
from jrnl.Journal import Journal
from jrnl.Journal import LegacyJournal
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg
from jrnl.prompt import create_password


def make_key(password):
    password = password.encode("utf-8")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        # Salt is hard-coded
        salt=b"\xf2\xd5q\x0e\xc1\x8d.\xde\xdc\x8e6t\x89\x04\xce\xf8",
        iterations=100_000,
        backend=default_backend(),
    )
    key = kdf.derive(password)
    return base64.urlsafe_b64encode(key)


def decrypt_content(
    decrypt_func: Callable[[str], Optional[str]],
    keychain: str = None,
    max_attempts: int = 3,
) -> str:
    def get_pw():
        return print_msg(
            Message(MsgText.Password, MsgStyle.PROMPT), get_input=True, hide_input=True
        )

    pwd_from_keychain = keychain and get_keychain(keychain)
    password = pwd_from_keychain or get_pw()
    result = decrypt_func(password)
    # Password is bad:
    if result is None and pwd_from_keychain:
        set_keychain(keychain, None)
    attempt = 1
    while result is None and attempt < max_attempts:
        print_msg(Message(MsgText.WrongPasswordTryAgain, MsgStyle.WARNING))
        password = get_pw()
        result = decrypt_func(password)
        attempt += 1

    if result is None:
        raise JrnlException(Message(MsgText.PasswordMaxTriesExceeded, MsgStyle.ERROR))

    return result


class EncryptedJournal(Journal):
    def __init__(self, name="default", **kwargs):
        super().__init__(name, **kwargs)
        self.config["encrypt"] = True
        self.password = None

    def open(self, filename=None):
        """Opens the journal file defined in the config and parses it into a list of Entries.
        Entries have the form (date, title, body)."""
        filename = filename or self.config["journal"]
        dirname = os.path.dirname(filename)
        if not os.path.exists(filename):
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
                print_msg(
                    Message(
                        MsgText.DirectoryCreated,
                        MsgStyle.NORMAL,
                        {"directory_name": dirname},
                    )
                )
            self.create_file(filename)
            self.password = create_password(self.name)

            print_msg(
                Message(
                    MsgText.JournalCreated,
                    MsgStyle.NORMAL,
                    {"journal_name": self.name, "filename": filename},
                )
            )

        text = self._load(filename)
        self.entries = self._parse(text)
        self.sort()
        logging.debug("opened %s with %d entries", self.__class__.__name__, len(self))
        return self

    def _load(self, filename):
        """Loads an encrypted journal from a file and tries to decrypt it.
        If password is not provided, will look for password in the keychain
        and otherwise ask the user to enter a password up to three times.
        If the password is provided but wrong (or corrupt), this will simply
        return None."""
        with open(filename, "rb") as f:
            journal_encrypted = f.read()

        def decrypt_journal(password):
            key = make_key(password)
            try:
                plain = Fernet(key).decrypt(journal_encrypted).decode("utf-8")
                self.password = password
                return plain
            except (InvalidToken, IndexError):
                return None

        if self.password:
            return decrypt_journal(self.password)

        return decrypt_content(keychain=self.name, decrypt_func=decrypt_journal)

    def _store(self, filename, text):
        key = make_key(self.password)
        journal = Fernet(key).encrypt(text.encode("utf-8"))
        with open(filename, "wb") as f:
            f.write(journal)

    @classmethod
    def from_journal(cls, other: Journal):
        new_journal = super().from_journal(other)
        new_journal.password = (
            other.password
            if hasattr(other, "password")
            else create_password(other.name)
        )

        return new_journal


class LegacyEncryptedJournal(LegacyJournal):
    """Legacy class to support opening journals encrypted with the jrnl 1.x
    standard. You'll not be able to save these journals anymore."""

    def __init__(self, name="default", **kwargs):
        super().__init__(name, **kwargs)
        self.config["encrypt"] = True
        self.password = None

    def _load(self, filename):
        with open(filename, "rb") as f:
            journal_encrypted = f.read()
        iv, cipher = journal_encrypted[:16], journal_encrypted[16:]

        def decrypt_journal(password):
            decryption_key = hashlib.sha256(password.encode("utf-8")).digest()
            decryptor = Cipher(
                algorithms.AES(decryption_key), modes.CBC(iv), default_backend()
            ).decryptor()
            try:
                plain_padded = decryptor.update(cipher) + decryptor.finalize()
                self.password = password
                if plain_padded[-1] in (" ", 32):
                    # Ancient versions of jrnl. Do not judge me.
                    return plain_padded.decode("utf-8").rstrip(" ")
                else:
                    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
                    plain = unpadder.update(plain_padded) + unpadder.finalize()
                    return plain.decode("utf-8")
            except ValueError:
                return None

        if self.password:
            return decrypt_journal(self.password)
        return decrypt_content(keychain=self.name, decrypt_func=decrypt_journal)


def get_keychain(journal_name):
    import keyring

    try:
        return keyring.get_password("jrnl", journal_name)
    except keyring.errors.KeyringError as e:
        if not isinstance(e, keyring.errors.NoKeyringError):
            print_msg(Message(MsgText.KeyringRetrievalFailure, MsgStyle.ERROR))
        return ""


def set_keychain(journal_name, password):
    import keyring

    if password is None:
        try:
            keyring.delete_password("jrnl", journal_name)
        except keyring.errors.KeyringError:
            pass
    else:
        try:
            keyring.set_password("jrnl", journal_name, password)
        except keyring.errors.KeyringError as e:
            if isinstance(e, keyring.errors.NoKeyringError):
                msg = Message(MsgText.KeyringBackendNotFound, MsgStyle.WARNING)
            else:
                msg = Message(MsgText.KeyringRetrievalFailure, MsgStyle.ERROR)
            print_msg(msg)
