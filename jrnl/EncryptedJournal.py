# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import hashlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes

from jrnl.Journal import LegacyJournal


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
