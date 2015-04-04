from . import Journal, util
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64


def make_key(password):
    if type(password) is unicode:
        password = password.encode('utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        # Salt is hard-coded
        salt='\xf2\xd5q\x0e\xc1\x8d.\xde\xdc\x8e6t\x89\x04\xce\xf8',
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password)
    return base64.urlsafe_b64encode(key)


class EncryptedJournal(Journal.Journal):
    def __init__(self, name='default', **kwargs):
        super(EncryptedJournal, self).__init__(name, **kwargs)
        self.config['encrypt'] = True

    def _load(self, filename, password=None):
        """Loads an encrypted journal from a file and tries to decrypt it.
        If password is not provided, will look for password in the keychain
        and otherwise ask the user to enter a password up to three times.
        If the password is provided but wrong (or corrupt), this will simply
        return None."""
        with open(filename) as f:
            journal_encrypted = f.read()

        def validate_password(password):
            key = make_key(password)
            try:
                return Fernet(key).decrypt(journal_encrypted).decode('utf-8')
            except (InvalidToken, IndexError):
                return None
        if password:
            return validate_password(password)
        return util.get_password(keychain=self.name, validator=validate_password)

    def _store(self, filename, text):
        key = make_key(self.config['password'])
        journal = Fernet(key).encrypt(text.encode('utf-8'))
        with open(filename, 'w') as f:
            f.write(journal)
