<!--
Copyright © 2012-2023 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# 設定ファイル参照

`jrnl`はYAML形式の設定ファイルに情報を保存します。

!!! note
編集前にジャーナルと設定ファイルをバックアップしてください。設定ファイルの
変更はジャーナルに破壊的な影響を与える可能性があります！

## 設定ファイルの場所

以下のコマンドを実行すると、設定ファイルの場所を確認できます：
`jrnl --list`

デフォルトでは、設定ファイルは`~/.config/jrnl/jrnl.yaml`にあります。
`XDG_CONFIG_HOME`変数が設定されている場合、設定ファイルは
`$XDG_CONFIG_HOME/jrnl/jrnl.yaml`として保存されます。

!!! note
Windowsでは、設定ファイルは通常
`%USERPROFILE%\.config\jrnl\jrnl.yaml`にあります。

## 設定フォーマット

設定ファイルは[YAML](https://yaml.org/)形式で、テキストエディタで編集できます。

## 設定キー

### journals

`jrnl`が使用する各ジャーナルを記述します。このキーの後の各インデントされたキーは
ジャーナルの名前です。

ジャーナルキーに値がある場合、その値はジャーナルへのパスとして解釈されます。
そうでない場合、ジャーナルはパスを指定するための追加のインデントされた
`journal`キーが必要です。

以下のすべてのキーは、`journal`キーと同じレベルで各ジャーナルに対して指定できます。
キーがトップレベルのキーと競合する場合、ジャーナル固有のキーが代わりに使用されます。

### editor

設定されている場合、このコマンドを実行して外部エディタを起動し、
エントリーの作成と編集を行います。一時ファイルへのパスがその後に
渡され、エディタが制御を`jrnl`に戻すと、`jrnl`がファイルを処理します。

一部のエディタは`jrnl`で動作するためにブロッキングプロセスである必要があるため、
特別なオプションが必要です。詳細は[外部エディタ](external-editors.md)を参照してください。

### encrypt

`true`の場合、AESを使用してジャーナルを暗号化します。既にデータがある
ジャーナルでは、この値を変更しないでください。

### template

新しいエントリーのテンプレートとして使用するテキストファイルへのパス。`editor`フィールドが
設定されている場合のみ機能します。テンプレートを使用する場合、エディタの
[一時ファイル](privacy-and-security.md#files-in-transit-from-editor-to-jrnl)は
テンプレートと同じ拡張子を持ちます。

### tagsymbols

タグとして解釈されるシンボル。

!!! note
タグに`#`文字を使用するのが直感的に思えますが、欠点があります：ほとんどの
シェルでは、これはコメントを開始するメタ文字として解釈されます。つまり、
以下のように入力すると：

    > `jrnl Implemented endless scrolling on the #frontend of our website.`

    bashは`#`以降をすべて切り捨てて`jrnl`に渡します。これを避けるには、
    入力を次のように引用符で囲みます：

    > `jrnl "Implemented endless scrolling on the #frontend of our website."`

    または、組み込みのプロンプトや外部エディタを使用してエントリーを
    作成してください。

### default_hour と default_minute

日付を指定しても具体的な時間を指定しない場合（例：`last thursday`）、エントリーはこの時間に作成されます。

### timeformat

ジャーナルに保存されるタイムスタンプの形式を定義します。
参照は[pythonドキュメント](http://docs.python.org/library/time.html#time.strftime)を確認してください。

既存のジャーナルでは変更しないでください。データ損失につながる可能性があります。

!!! note
`jrnl`は`%z`または`%Z`タイムゾーン識別子をサポートしていません。

### highlight

`true`の場合、タグはシアン色で強調表示されます。

### linewrap

出力の幅を制御します。長い行を折り返したくない場合は`false`に設定します。
`jrnl`に自動的に端末幅を決定させる場合は`auto`に設定します。

### colors

ジャーナルエントリーの表示に使用される色を制御する辞書です。
4つのサブキーがあります：`body`、`date`、`tags`、`title`。

現在有効な値は：`BLACK`、`RED`、`GREEN`、`YELLOW`、`BLUE`、
`MAGENTA`、`CYAN`、`WHITE`、`NONE`です。

色付けには`colorama.Fore`が使用され、[ドキュメントはこちら](https://github.com/tartley/colorama#colored-output)で確認できます。

色付き出力を無効にするには、値を`NONE`に設定します。

### display_format

デフォルトで使用するフォーマッタを指定します。[フォーマット](formats.md)を参照してください。

### version

`jrnl`は自動的にこのフィールドを実行中のバージョンに更新します。
このフィールドを手動で変更する必要はありません。
