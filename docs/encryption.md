<!--
Copyright (C) 2012-2022 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# Encryption

## A Note on Security

While `jrnl` follows best practices, total security is never possible in the
real world. There are a number of ways that people can at least partially
compromise your `jrnl` data. See the [Privacy and Security](./privacy-and-security.md) page
for more information.

## Encrypting and Decrypting

Existing plain text journal files can be encrypted using the `--encrypt`
command:

``` sh
jrnl --encrypt [FILENAME]
```

You can then enter a new password, and the unencrypted file will replaced with
the new encrypted file.

This command also works to change the password for a journal file that is
already encrypted. `jrnl` will prompt you for the current password and then new
password.

Conversely,

``` sh
jrnl --decrypt [FILENAME]
```

replaces the encrypted journal file with a plain text file. You can also specify
a filename, e.g., `jrnl --decrypt plain_text_copy.txt`, to leave the original
encrypted file untouched and create a new plain text file next to it.

!!! note
    Changing `encrypt` in your [config file](./reference-config-file.md) to
    a different value will not encrypt or decrypt your
    journal file. It merely says whether or not your journal
    is encrypted. Hence manually changing
    this option will most likely result in your journal file being
    impossible to load. This is why the above commands are necessary.

## Storing Passwords in Your Keychain

Nobody can recover or reset your `jrnl` password. If you lose it,
your data will be inaccessible forever.

For this reason, when encrypting a journal, `jrnl` asks whether you would like
to store the password in your system's keychain. An added benefit is that you
will not need to enter the password when interacting with the journal file.

If you don't initially store the password in your keychain but decide to do so
later---or if you want to store it in one computer's keychain but not in another
computer's---you can run `jrnl --encrypt` on an encrypted journal and use the
same password again. This will trigger the keychain storage prompt.

## Manual Decryption

The easiest way to decrypt your journal is with `jrnl --decrypt`, but you could
also decrypt your journal manually if needed. To do this, you can use any
program that supports the AES algorithm (specifically AES-CBC), and you'll need
the following relevant information for decryption:

- **Key:** The key used for encryption is the
    [SHA-256](https://en.wikipedia.org/wiki/SHA-2) hash of your password.
- **Initialization vector (IV):** The IV is stored in the first 16 bytes of
    your encrypted journal file.
- **The actual text of the journal** (everything after the first 16 bytes in
    the encrypted journal file) is encoded in
    [UTF-8](https://en.wikipedia.org/wiki/UTF-8) and padded according to
    [PKCS\#7](https://en.wikipedia.org/wiki/PKCS_7) before being encrypted.

If you'd like an example of what this might look like in script form, please
see below for some examples of Python scripts that you could use to manually
decrypt your journal.



!!! note
    These are only examples, and are only here to illustrate that your journal files
    will still be recoverable even if `jrnl` isn't around anymore. Please use 
    `jrnl --decrypt` if available.

**Example for jrnl v2 files**:
``` python
#!/usr/bin/env python3
"""
Decrypt a jrnl v2 encrypted journal.

Note: the `cryptography` module must be installed (you can do this with
something like `pip3 install crytography`)
"""

import base64
import getpass
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


filepath = input("journal file path: ")
password = getpass.getpass("Password: ")

with open(Path(filepath),"rb") as f:
    ciphertext = f.read()

password = password.encode("utf-8")
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b"\xf2\xd5q\x0e\xc1\x8d.\xde\xdc\x8e6t\x89\x04\xce\xf8",
    iterations=100_000,
    backend=default_backend(),
)

key = base64.urlsafe_b64encode(kdf.derive(password))

print(Fernet(key).decrypt(ciphertext).decode('utf-8'))
```

**Example for jrnl v1 files**:
``` python
#!/usr/bin/env python3
"""
Decrypt a jrnl v1 encrypted journal.

Note: the `pycrypto` module must be installed (you can do this with something
like `pip3 install pycrypto`)
"""

import argparse
from Crypto.Cipher import AES
import getpass
import hashlib
import sys

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="journal file to decrypt")
args = parser.parse_args()

pwd = getpass.getpass()
key = hashlib.sha256(pwd.encode('utf-8')).digest()

with open(args.filepath, 'rb') as f:
    ciphertext = f.read()

crypto = AES.new(key, AES.MODE_CBC, ciphertext[:16])
plain = crypto.decrypt(ciphertext[16:])
plain = plain.strip(plain[-1:])
plain = plain.decode("utf-8")
print(plain)
```
