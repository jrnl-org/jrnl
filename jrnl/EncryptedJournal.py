from . import util
from .Journal import Journal, LegacyJournal
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import sys
import os
import base64
import logging
from typing import Optional


log = logging.getLogger()


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


class EncryptedJournal(Journal):
    def __init__(self, name="default", **kwargs):
        super().__init__(name, **kwargs)
        self.config["encrypt"] = True
        self.password = None

    def open(self, filename=None):
        """Opens the journal file defined in the config and parses it into a list of Entries.
        Entries have the form (date, title, body)."""
        filename = filename or self.config["journal"]

        if not os.path.exists(filename):
            self.create_file(filename)
            self.password = util.create_password(self.name)
            print(
                f"Encrypted journal '{self.name}' created at {filename}",
                file=sys.stderr,
            )

        text = self._load(filename)
        self.entries = self._parse(text)
        self.sort()
        log.debug("opened %s with %d entries", self.__class__.__name__, len(self))
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

        return util.decrypt_content(keychain=self.name, decrypt_func=decrypt_journal)

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
            else util.create_password(other.name)
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
        return util.decrypt_content(keychain=self.name, decrypt_func=decrypt_journal)
