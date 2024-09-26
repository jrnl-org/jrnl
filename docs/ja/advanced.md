<!--
Copyright © 2012-2023 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# 高度な使用方法

## 設定ファイル

`jrnl`には、テンプレート、フォーマット、複数のジャーナルなど、設定ファイルを通
してカスタマイズできる多様なオプションがあります。詳細については[設定ファイルリ
ファレンス](./reference-config-file.md)を参照するか、以下の一般的な使用例をお読
みください。

### 複数のジャーナルファイル

[設定ファイル](./reference-config-file.md)でより多くのジャーナルを定義することで、`jrnl`を複数のジャーナル（例：`private`と`work`）で使用するように設定できます。例えば：

```yaml
journals:
  default: ~/journal.txt
  work: ~/work.txt
```

`default`ジャーナルは`jrnl`を初めて起動したときに作成されます。
これで、`jrnl`の代わりに`jrnl work`を使用して`work`ジャーナルにアクセスできます。例えば：

```sh
jrnl work at 10am: @Steveとのミーティング
jrnl work -n 3
```

これらはどちらも`~/work.txt`を使用しますが、`jrnl -n 3`は`~/journal.txt`から最後の3つのエントリーを表示します（`jrnl default -n 3`も同様です）。

各ジャーナルのデフォルトオプションを個別にオーバーライドすることもできます。
`jrnl.yaml`が以下のようになっている場合：

```yaml
encrypt: false
journals:
  default: ~/journal.txt
  work:
    journal: ~/work.txt
    encrypt: true
  food: ~/my_recipes.txt
```

`default`と`food`ジャーナルは暗号化されませんが、`work`ジャーナルは暗号化されます！

`jrnl.yaml`のトップレベルにあるすべてのオプションをオーバーライドできますが、少なくともそのジャーナルのジャーナルファイルを指す`journal: ...`キーを指定してください。

以下の設定例を考えてみましょう：

```yaml
editor: vi -c startinsert
journals:
  default: ~/journal.txt
  work:
    journal: ~/work.txt
    encrypt: true
    display_format: json
    editor: code -rw
  food:
    display_format: markdown
    journal: ~/recipes.txt
```

`work`ジャーナルは暗号化され、デフォルトで`json`形式で出力され、VSCodeの既存のウィンドウで編集されます。同様に、`food`ジャーナルはデフォルトでmarkdown形式で出力されますが、他のすべてのデフォルト設定を使用します。

### コマンドラインから設定を変更する

現在の`jrnl`インスタンスの設定フィールドを`--config-override CONFIG_KEY CONFIG_VALUE`を使用してオーバーライドできます。ここで、`CONFIG_KEY`は有効な設定フィールドをドット表記で指定し、`CONFIG_VALUE`は希望する（有効な）オーバーライド値です。ドット表記を使用して、`colors.title`のような他のキー内のキーを変更することもできます。

複数のオーバーライドを指定するには、`--config-override`を複数回呼び出します。

!!! note
これらのオーバーライドにより、jrnl設定の**_任意の_**フィールドを変更できます。自己責任で使用してください。

#### 例

```sh
# 高速ログ記録のために`stdin`プロンプトを使用してエントリーを作成する
jrnl --config-override editor ""

# プロジェクトのログを記録する
jrnl --config-override journals.todo "$(git rev-parse --show-toplevel)/todo.txt" todo タオルを見つける

# 複数のオーバーライドを渡す
jrnl --config-override display_format fancy --config-override linewrap 20 \
--config-override colors.title green
```

### 代替設定の使用

現在の`jrnl`インスタンスに対して、`--config-file CONFIG_FILE_PATH`を使用して代替設定ファイルを指定できます。ここで`CONFIG_FILE_PATH`は代替`jrnl`設定ファイルへのパスです。

#### 例

```sh
# 個人的なジャーナルエントリーに個人用設定ファイルを使用する
jrnl --config-file ~/foo/jrnl/personal-config.yaml

# 仕事関連のエントリーに代替設定ファイルを使用する
jrnl --config-file ~/foo/jrnl/work-config.yaml

# デフォルトの設定ファイルを使用する（初回実行時に作成される）
jrnl
```
