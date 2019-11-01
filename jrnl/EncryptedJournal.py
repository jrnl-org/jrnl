from . import Journal, util
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

log = logging.getLogger()


def make_key(password):
    password = password.encode("utf-8")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        # Salt is hard-coded
        salt=b'\xf2\xd5q\x0e\xc1\x8d.\xde\xdc\x8e6t\x89\x04\xce\xf8',
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password)
    return base64.urlsafe_b64encode(key)


class EncryptedJournal(Journal.Journal):
    def __init__(self, name='default', **kwargs):
        super().__init__(name, **kwargs)
        self.config['encrypt'] = True

    def open(self, filename=None):
        """Opens the journal file defined in the config and parses it into a list of Entries.
        Entries have the form (date, title, body)."""
        filename = filename or self.config['journal']

        if not os.path.exists(filename):
            password = util.getpass("Enter password for new journal: ")
            if password:
                if util.yesno("Do you want to store the password in your keychain?", default=True):
                    util.set_keychain(self.name, password)
                else:
                    util.set_keychain(self.name, None)
                self.config['password'] = password
                text = ""
                self._store(filename, text)
                print(f"[Journal '{self.name}' created at {filename}]", file=sys.stderr)
            else:
                print("No password supplied for encrypted journal", file=sys.stderr)
                sys.exit(1)
        else:
            text = self._load(filename)
        self.entries = self._parse(text)
        self.sort()
        log.debug("opened %s with %d entries", self.__class__.__name__, len(self))
        return self

    def _load(self, filename, password=None):
        """Loads an encrypted journal from a file and tries to decrypt it.
        If password is not provided, will look for password in the keychain
        and otherwise ask the user to enter a password up to three times.
        If the password is provided but wrong (or corrupt), this will simply
        return None."""
        with open(filename, 'rb') as f:
            journal_encrypted = f.read()

        def validate_password(password):
            key = make_key(password)
            try:
                plain = Fernet(key).decrypt(journal_encrypted).decode('utf-8')
                self.config['password'] = password
                return plain
            except (InvalidToken, IndexError):
                return None
        if password:
            return validate_password(password)
        return util.get_password(keychain=self.name, validator=validate_password)

    def _store(self, filename, text):
        key = make_key(self.config['password'])
        journal = Fernet(key).encrypt(text.encode('utf-8'))
        with open(filename, 'wb') as f:
            f.write(journal)

    @classmethod
    def _create(cls, filename, password):
        key = make_key(password)
        dummy = Fernet(key).encrypt(b"")
        with open(filename, 'wb') as f:
            f.write(dummy)


class LegacyEncryptedJournal(Journal.LegacyJournal):
    """Legacy class to support opening journals encrypted with the jrnl 1.x
    standard. You'll not be able to save these journals anymore."""
    def __init__(self, name='default', **kwargs):
        super().__init__(name, **kwargs)
        self.config['encrypt'] = True

    def _load(self, filename, password=None):
        with open(filename, 'rb') as f:
            journal_encrypted = f.read()
        iv, cipher = journal_encrypted[:16], journal_encrypted[16:]

        def validate_password(password):
            decryption_key = hashlib.sha256(password.encode('utf-8')).digest()
            decryptor = Cipher(algorithms.AES(decryption_key), modes.CBC(iv), default_backend()).decryptor()
            try:
                plain_padded = decryptor.update(cipher) + decryptor.finalize()
                self.config['password'] = password
                if plain_padded[-1] in (" ", 32):
                    # Ancient versions of jrnl. Do not judge me.
                    return plain_padded.decode('utf-8').rstrip(" ")
                else:
                    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
                    plain = unpadder.update(plain_padded) + unpadder.finalize()
                    return plain.decode('utf-8')
            except ValueError:
                return None
        if password:
            return validate_password(password)
        return util.get_password(keychain=self.name, validator=validate_password)
