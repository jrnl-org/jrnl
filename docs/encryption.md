# Encryption

## Encrypting and decrypting

If you don’t choose to encrypt your file when you run
`jrnl` for the first time, you can encrypt
your existing journal file or change its password using this:

``` sh
jrnl --encrypt
```

If it is already encrypted, you will first be asked for the current
password. You can then enter a new password and your plain journal will
replaced by the encrypted file. Conversely,

``` sh
jrnl --decrypt
```

will replace your encrypted journal file with a journal in plain text. You
can also specify a filename, i.e. `jrnl --decrypt plain_text_copy.txt`,
to leave your original file untouched.

## Storing passwords in your keychain

Whenever you encrypt your journal, you are asked whether you want to
store the encryption password in your keychain. If you do this, you
won’t have to enter your password every time you want to write or read
your journal.

If you don’t initially store the password in the keychain but decide to
do so at a later point – or maybe want to store it on one computer but
not on another – you can run `jrnl --encrypt` on an encrypted
journal and use the same password again.

## A note on security

While `jrnl` follows best practices, total security is an illusion.
There are a number of ways that people can at least partially
compromise your `jrnl` data. See the [Privacy and Security](./security.md)
documentation for more information.

## No password recovery

There is no method to recover or reset your `jrnl` password. If you lose it,
your data is inaccessible.

## Manual decryption

Should you ever want to decrypt your journal manually, you can do so
with any program that supports the AES algorithm in CBC. The key used
for encryption is the SHA-256-hash of your password, the IV
(initialisation vector) is stored in the first 16 bytes of the encrypted
file. The plain text is encoded in UTF-8 and padded according to PKCS\#7
before being encrypted. Here’s a Python script that you can use to
decrypt your journal:

``` python
#!/usr/bin/env python3

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
