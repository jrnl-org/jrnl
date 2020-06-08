# Encryption

## `pycrypto`

Please note that _all_ of `jrnl`'s encryption functions require `pycrypto`,
which can be installed using `pip`:

```sh
pip3 install pycrypto
```

## Encrypting and Decrypting

If you chose not to encrypt your file when you ran `jrnl` for the first time,
you can still encrypt your existing journal file or change its password using
the following command:

``` sh
jrnl --encrypt
```

If your file is already encrypted, you will first be asked for the current
password. You can then enter a new password, and your unencrypted file will
replaced with the new encrypted file. Conversely,

``` sh
jrnl --decrypt
```

replaces your encrypted journal file with a journal in plain text. You can also
specify a filename, e.g., `jrnl --decrypt plain_text_copy.txt`, to leave the
original encrypted file untouched and create a new plain text file next to it.

## Storing Passwords in Your Keychain

When you encrypt your journal, you will be asked whether you want to store the
encryption password in your keychain. This saves you the trouble of having to
enter your password every time you want to write in or read your journal.

If you don't initially store the password in the keychain but decide to do so at
a later point---or if you want to store it in one computer's keychain but not
in another computer's---you can run `jrnl --encrypt` on an encrypted journal
and use the same password again. This will trigger the keychain storage prompt.

## A Note on Security

While `jrnl` follows best practices, total security is never possible in the
real world. There are a number of ways that people can at least partially
compromise your `jrnl` data. See the [Privacy and Security](./security.md)
page for more information.

## Password Recovery

There is no method to recover or reset your `jrnl` password. If you lose it,
your data is inaccessible forever.

## Manual Decryption

Should you ever want to decrypt your journal manually, you can do so with any
program that supports the AES algorithm in CBC. The key used for encryption is
the SHA-256 hash of your password. The IV (initialization vector) is stored in
the first 16 bytes of the encrypted file. The plain text is encoded in UTF-8 and
padded according to PKCS\#7 before being encrypted.

Here is a Python script that you can use to decrypt your journal:

``` python
#!/usr/bin/env python3

import argparse
from Crypto.Cipher import AES
import getpass
import hashlib
import sys

parser = argparse.ArgumentParser()
parser.add_argument(“filepath”, help=”journal file to decrypt”)
args = parser.parse_args()

pwd = getpass.getpass()
key = hashlib.sha256(pwd.encode(‘utf-8’)).digest()

with open(args.filepath, ‘rb’) as f:
    ciphertext = f.read()

crypto = AES.new(key, AES.MODE_CBC, ciphertext[:16])
plain = crypto.decrypt(ciphertext[16:])
plain = plain.strip(plain[-1:])
plain = plain.decode(“utf-8”)
print(plain)
```
