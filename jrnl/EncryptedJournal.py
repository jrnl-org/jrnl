from . import Journal, util
from cryptography.fernet import Fernet, InvalidToken
import base64
from passlib.hash import pbkdf2_sha256


def make_key(password):
    derived_key = pbkdf2_sha256.encrypt(password.encode("utf-8"), rounds=10000, salt_size=16)
    return base64.urlsafe_b64encode(derived_key)


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
