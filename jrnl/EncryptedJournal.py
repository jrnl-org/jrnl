import hashlib
import sys
from . import Journal, util
try:
    from Crypto.Cipher import AES
    from Crypto import Random
    crypto_installed = True
except ImportError:
    crypto_installed = False


def make_key(password):
    return hashlib.sha256(password.encode("utf-8")).digest()


def _decrypt(cipher, key):
    """Decrypts a cipher string using self.key as the key and the first 16 byte of the cipher as the IV"""
    if not crypto_installed:
        sys.exit("Error: PyCrypto is not installed.")
    if not cipher:
        return ""
    crypto = AES.new(key, AES.MODE_CBC, cipher[:16])
    try:
        plain = crypto.decrypt(cipher[16:])
    except ValueError:
        util.prompt("ERROR: Your journal file seems to be corrupted. You do have a backup, don't you?")
        sys.exit(1)

    padding_length = util.byte2int(plain[-1])
    if padding_length > AES.block_size and padding_length != 32:
        # 32 is the space character and is kept for backwards compatibility
        return None
    elif padding_length == 32:
        plain = plain.strip()
    elif plain[-padding_length:] != util.int2byte(padding_length) * padding_length:
        # Invalid padding!
        return None
    else:
        plain = plain[:-padding_length]

    return plain.decode("utf-8")


def _encrypt(plain, key):
    """Encrypt a plaintext string using key"""
    if not crypto_installed:
        sys.exit("Error: PyCrypto is not installed.")
    Random.atfork()  # A seed for PyCrypto
    iv = Random.new().read(AES.block_size)
    crypto = AES.new(key, AES.MODE_CBC, iv)
    plain = plain.encode("utf-8")
    padding_length = AES.block_size - len(plain) % AES.block_size
    plain += util.int2byte(padding_length) * padding_length
    return iv + crypto.encrypt(plain)


class EncryptedJournal(Journal.Journal):
    def __init__(self, name='default', **kwargs):
        super(EncryptedJournal, self).__init__(name, **kwargs)
        self.config['encrypt'] = True

    def _load(self, filename):
        with open(filename, "rb") as f:
            journal_encrypted = f.read()

        def validate_password(password):
            key = make_key(password)
            return _decrypt(journal_encrypted, key)

        text = None

        if 'password' in self.config:
            text = validate_password(self.config['password'])

        if text is None:
            text = util.get_password(keychain=self.name, validator=validate_password)

        return text

    def _store(self, filename, text):
        key = make_key(self.config['password'])
        journal = _encrypt(text, key)

        with open(filename, 'wb') as f:
            f.write(journal)
