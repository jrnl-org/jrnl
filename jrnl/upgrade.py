from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib
import util
from . import __version__
import sys

def upgrade_encrypted_journal(filename, key_plain):
    """Decrypts a journal in memory using the jrnl 1.x encryption scheme
    and returns it in plain text."""
    with open(filename) as f:
        iv_cipher = f.read()
    iv, cipher = iv_cipher[:16], iv_cipher[16:]
    decryption_key = hashlib.sha256(key_plain.encode('utf-8')).digest()
    decryptor = Cipher(algorithms.AES(decryption_key), modes.CBC(iv), default_backend())
    plain_padded = decryptor.update(cipher)
    try:
        plain_padded += decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plain = unpadder.update(plain_padded)
        plain += unpadder.finalize()
    except ValueError:
        return None
    return plain


def upgrade_jrnl_if_necessary(config_path):
    with open(config_path) as f:
        config = f.read()
    if not config.strip().startswith("{"):
        return

    util.prompt("Welcome to jrnl {}".format(__version__))
    util.prompt("jrnl will now upgrade your configuration and journal files.")
    util.prompt("Please note that jrnl 1.x is NOT forward compatible with this version of jrnl.")
    util.prompt("If you choose to proceed, you will not be able to use your journals with")
    util.prompt("older versions of jrnl anymore.")
    cont = util.yesno("Continue upgrading jrnl?", default=False)
    if not cont:
        util.prompt("jrnl NOT upgraded, exiting.")
        sys.exit(1)

    util.prompt("")
