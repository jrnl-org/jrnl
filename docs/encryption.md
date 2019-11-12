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
not on another – you can simply run `jrnl --encrypt` on an encrypted
journal and use the same password again.

## A note on security

While jrnl follows best practises, true security is an illusion.
Specifically, jrnl will leave traces in your memory and your shell
history – it’s meant to keep journals secure in transit, for example
when storing it on an
[untrusted](http://techcrunch.com/2014/04/09/condoleezza-rice-joins-dropboxs-board/)
services such as Dropbox. If you’re concerned about security, disable
history logging for journal in your `.bashrc`:

``` sh
HISTIGNORE="$HISTIGNORE:jrnl *"
```

If you are using zsh instead of bash, you can get the same behaviour by
adding this to your `zshrc`:

``` sh
setopt HIST_IGNORE_SPACE
alias jrnl=" jrnl"
```

The fish shell does not support automatically preventing logging like
this. To prevent `jrnl` commands being logged by fish, you must make
sure to type a space before every `jrnl` command you enter. To delete
existing `jrnl` commands from fish’s history, run
`history delete --prefix 'jrnl '`.

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
