import hashlib
from . import Journal, util
from cryptography.fernet import Fernet, InvalidToken
import base64


def make_key(password):
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode("utf-8")).digest())


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
                return Fernet(key).decrypt(journal_encrypted)
            except InvalidToken:
                return None

        return util.get_password(keychain=self.name, validator=validate_password)

    def _store(self, filename, text):
        key = make_key(self.config['password'])
        journal = Fernet(key).encrypt(text)
        with open(filename, 'w') as f:
            f.write(journal)
