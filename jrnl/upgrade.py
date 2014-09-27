from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib
import util
from . import __version__
from . import EncryptedJournal
import sys
from cryptography.fernet import Fernet


def upgrade_encrypted_journal(filename, key_plain):
    """Decrypts a journal in memory using the jrnl 1.x encryption scheme
    and returns it in plain text."""
    util.prompt( "UPGRADING JOURNAL")
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

    key = EncryptedJournal.make_key(key_plain)
    journal = Fernet(key).encrypt(plain.encode('utf-8'))
    with open(filename, 'w') as f:
        f.write(journal)
    return plain


def upgrade_jrnl_if_necessary(config_path):
    with open(config_path) as f:
        config = f.read()
    if not config.strip().startswith("{"):
        return

    config = util.load_config(config_path)

    util.prompt("""Welcome to jrnl {}
                jrnl will now upgrade your configuration and journal files.
                Please note that jrnl 1.x is NOT forward compatible with this version of jrnl.
                If you choose to proceed, you will not be able to use your journals with
                older versions of jrnl anymore.""".format(__version__))

    encrypted_journals = {}
    plain_journals = {}
    for journal, journal_conf in config['journals'].items():
        if isinstance(journal_conf, dict):
            if journal_conf.get("encrypt"):
                encrypted_journals[journal] = journal_conf.get("journal")
            else:
                plain_journals[journal] = journal_conf.get("journal")
        else:
            if config.get('encrypt'):
                encrypted_journals[journal] = journal_conf
            else:
                plain_journals[journal] = journal_conf
    if encrypted_journals:
        util.prompt("Following encrypted journals will be upgraded to jrnl {}:".format(__version__))
        for journal, path in encrypted_journals.items():
            util.prompt("    {:20} -> {}".format(journal, path))
        if plain_journals:
            util.prompt("Following plain text journals will be not be touched:")
            for journal, path in plain_journals.items():
                util.prompt("    {:20} -> {}".format(journal, path))

    cont = util.yesno("Continue upgrading jrnl?", default=False)
    if not cont:
        util.prompt("jrnl NOT upgraded, exiting.")
        sys.exit(1)

    for journal, path in encrypted_journals.items():
        util.prompt("Enter password for {} journal (stored in {}).".format(journal, path))
        util.get_password(keychain=journal, validator=lambda pwd: upgrade_encrypted_journal(path, pwd))
