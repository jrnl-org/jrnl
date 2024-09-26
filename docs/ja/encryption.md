<!--
Copyright © 2012-2023 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# 暗号化

## セキュリティに関する注意

`jrnl`はベストプラクティスに従っていますが、現実世界で完全なセキュリティを実現することは不可能です。あなたの`jrnl`データを少なくとも部分的に侵害する方法はいくつかあります。詳細については、[プライバシーとセキュリティ](./privacy-and-security.md)のページを参照してください。

## 暗号化と復号化

既存のプレーンテキストのジャーナルファイルは、`--encrypt`コマンドを使用して暗号化できます：

```sh
jrnl --encrypt [ファイル名]
```

その後、新しいパスワードを入力すると、暗号化されていないファイルが新しい暗号化されたファイルに置き換えられます。

このコマンドは、既に暗号化されているジャーナルファイルのパスワードを変更する際にも機能します。`jrnl`は現在のパスワードと新しいパスワードの入力を求めます。

逆に、

```sh
jrnl --decrypt [ファイル名]
```

は暗号化されたジャーナルファイルをプレーンテキストファイルに置き換えます。また、ファイル名を指定することもできます（例：`jrnl --decrypt plain_text_copy.txt`）。これにより、元の暗号化されたファイルはそのままで、その隣に新しいプレーンテキストファイルが作成されます。

!!! note
[設定ファイル](./reference-config-file.md)の`encrypt`を別の値に変更しても、
ジャーナルファイルの暗号化や復号化は行われません。それはただ、あなたの
ジャーナルが暗号化されているかどうかを示すだけです。したがって、この
オプションを手動で変更すると、ほとんどの場合、ジャーナルファイルを
ロードできなくなります。そのため、上記のコマンドが必要になります。

## パスワードをキーチェーンに保存する

誰も`jrnl`のパスワードを回復またはリセットすることはできません。パスワードを失うと、
あなたのデータに永久にアクセスできなくなります。

このため、ジャーナルを暗号化する際、`jrnl`はパスワードをシステムのキーチェーンに
保存するかどうかを尋ねます。追加の利点として、ジャーナルファイルとやり取りする際に
パスワードを入力する必要がなくなります。

最初にパスワードをキーチェーンに保存しなかったが、後で保存することにした場合
（または、あるコンピューターのキーチェーンには保存したいが、別のコンピューターでは
保存したくない場合）、暗号化されたジャーナルに対して`jrnl --encrypt`を実行し、
同じパスワードを再度使用することができます。これによりキーチェーン保存のプロンプトが
トリガーされます。

## 手動復号化

ジャーナルを復号化する最も簡単な方法は`jrnl --decrypt`を使用することですが、
必要に応じてジャーナルを手動で復号化することもできます。これを行うには、
AESアルゴリズム（特にAES-CBC）をサポートする任意のプログラムを使用できます。
復号化には以下の関連情報が必要です：

- **キー：** 暗号化に使用されるキーは、パスワードの
  [SHA-256](https://en.wikipedia.org/wiki/SHA-2)ハッシュです。
- **初期化ベクトル（IV）：** IVは暗号化されたジャーナルファイルの最初の16バイトに
  保存されています。
- **ジャーナルの実際のテキスト**（暗号化されたジャーナルファイルの最初の16バイト
  以降のすべて）は[UTF-8](https://en.wikipedia.org/wiki/UTF-8)でエンコードされ、
  暗号化される前に[PKCS#7](https://en.wikipedia.org/wiki/PKCS_7)に従って
  パディングされます。

スクリプト形式でどのように見えるかの例が必要な場合は、以下にジャーナルを手動で
復号化するのに使用できるPythonスクリプトの例をいくつか示します。

!!! note
これらは単なる例であり、`jrnl`が存在しなくなっても、ジャーナルファイルが
まだ復元可能であることを示すためにここにあります。可能な場合は
`jrnl --decrypt`を使用してください。

**jrnl v2ファイルの例**：

```python
#!/usr/bin/env python3
"""
jrnl v2の暗号化されたジャーナルを復号化します。

注意：`cryptography`モジュールがインストールされている必要があります
（`pip3 install crytography`のようなコマンドでインストールできます）
"""

import base64
import getpass
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

filepath = input("ジャーナルファイルのパス: ")
password = getpass.getpass("パスワード: ")

with open(Path(filepath), "rb") as f:
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

print(Fernet(key).decrypt(ciphertext).decode("utf-8"))
```

**jrnl v1ファイルの例**：

```python
#!/usr/bin/env python3
"""
jrnl v1の暗号化されたジャーナルを復号化します。

注意：`pycrypto`モジュールがインストールされている必要があります
（`pip3 install pycrypto`のようなコマンドでインストールできます）
"""

import argparse
import getpass
import hashlib

from Crypto.Cipher import AES

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="復号化するジャーナルファイル")
args = parser.parse_args()

pwd = getpass.getpass()
key = hashlib.sha256(pwd.encode("utf-8")).digest()

with open(args.filepath, "rb") as f:
    ciphertext = f.read()

crypto = AES.new(key, AES.MODE_CBC, ciphertext[:16])
plain = crypto.decrypt(ciphertext[16:])
plain = plain.strip(plain[-1:])
plain = plain.decode("utf-8")
print(plain)
```
