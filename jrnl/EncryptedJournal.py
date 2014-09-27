from . import Journal, util
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os


def make_key(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=os.urandom(16),
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password)
    return base64.urlsafe_b64encode(key)


class EncryptedJournal(Journal.Journal):
    def __init__(self, name='default', **kwargs):
        super(EncryptedJournal, self).__init__(name, **kwargs)
        self.config['encrypt'] = True

    def _load(self, filename):
        with open(filename) as f:
            journal_encrypted = f.read()

        def validate_password(password):
            key = make_key(password)
            try:
                return Fernet(key).decrypt(journal_encrypted).decode('utf-8')
            except (InvalidToken, IndexError):
                print base64.urlsafe_b64decode(journal_encrypted)
                return None

        return util.get_password(keychain=self.name, validator=validate_password)

    def _store(self, filename, text):
        key = make_key(self.config['password'])
        journal = Fernet(key).encrypt(text.encode('utf-8'))
        with open(filename, 'w') as f:
            f.write(journal)
