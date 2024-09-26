<!--
Copyright © 2012-2023 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# 外部エディタ

お好みの外部エディタを設定するには、[設定ファイル](./reference-config-file.md#editor)の`editor`オプションを更新してください。エディタがオペレーティングシステムの`PATH`環境変数に含まれていない場合は、エディタのフルパスを入力する必要があります。

設定が完了したら、`jrnl`コマンドを単独で使用して、エディタで新しいドキュメントとしてエントリーを作成できます：

```text
jrnl
```

ドキュメントの最初の行に、通常通りエントリーの時間とタイトルを指定できます。

クイックエントリーを含めることで、エディタをスキップすることもできます：

```text
jrnl yesterday: All my troubles seemed so far away.
```

コマンドラインでエントリーを開始し、選択したエディタで書き続けたい場合は、`--edit`フラグを使用します。例：

```text
jrnl yesterday: All my troubles seemed so far away. --edit
```

!!! note
エントリーの編集を保存してログに記録するには、ファイルを保存して閉じてください。

jrnlで動作するには、すべてのエディタが[ブロッキングプロセス](<https://en.wikipedia.org/wiki/Blocking_(computing)>)である必要があります。[micro](https://micro-editor.github.io/)のような一部のエディタはデフォルトでブロッキングですが、他のエディタは以下に記載されているような追加の引数でブロッキングにすることができます。jrnlがエディタを開いても即座に実行が終了する場合、そのエディタはブロッキングプロセスではありません。以下の提案のいずれかで修正できる可能性があります。

エディタが機密情報を漏洩する可能性とそのリスクを軽減する方法については、[このセクション](./privacy-and-security.md#editor-history)を参照してください。

## Sublime Text

[Sublime Text](https://www.sublimetext.com/)を使用するには、Sublime Textのコマンドラインツールをインストールし、`jrnl.yaml`を以下のように設定します：

```yaml
editor: "subl -w"
```

`-w`フラグは、jrnlがSublime Textがファイルを閉じるのを待ってからジャーナルに書き込むようにするためのものです。

## Visual Studio Code

[Visual Studio Code](https://code.visualstudio.com)も、プロセスがファイルを閉じるまで待機するように指示するフラグが必要です：

```yaml
editor: "code --wait"
```

Windowsでは、`code`はデフォルトでパスに追加されていないので、`code.exe`ファイルのフルパスを入力するか、`PATH`変数に追加する必要があります。

## MacVim

Sublime Textと同様に、MacVimもプロセスがファイルを閉じるまで待機してからジャーナルに制御を戻すように指示するフラグで起動する必要があります。MacVimの場合、このフラグは`-f`です：

```yaml
editor: "mvim -f"
```

## Vim/Neovim

Linuxでエディタとしてvimの派生版を使用するには、単純に`editor`を実行ファイルに設定します：

```yaml
editor: "vim"
# または
editor: "nvim"
```

## iA Writer

OS Xでは、素晴らしい[iA Writer](http://www.iawriter.com/mac)を使用してエントリーを書くことができます。`jrnl.yaml`を以下のように設定してください：

```yaml
editor: "open -b pro.writer.mac -Wn"
```

これは何をしているのでしょうか？`open -b ...`は、バンドル識別子（すべてのアプリに固有の文字列）で識別されるアプリケーションを使用してファイルを開きます。`-Wn`は、制御を戻す前にアプリケーションが閉じるまで待つこと、およびアプリケーションの新しいインスタンスを使用することをアプリケーションに指示します。

システムで`pro.writer.mac`バンドル識別子が見つからない場合は、シェルでiA Writerの`Info.plist`ファイルを調べることで、使用する正しい文字列を見つけることができます：

```sh
grep -A 1 CFBundleIdentifier /Applications/iA\ Writer.app/Contents/Info.plist
```

## Windows上のNotepad++

[Notepad++](http://notepad-plus-plus.org/)をエディタとして設定するには、`jrnl`の設定ファイル（`jrnl.yaml`）を以下のように編集します：

```yaml
editor: "C:\\Program Files (x86)\\Notepad++\\notepad++.exe -multiInst -nosession"
```

二重のバックスラッシュは、`jrnl`がファイルパスを正しく読み取るために必要です。`-multiInst -nosession`オプションにより、`jrnl`は独自のNotepad++ウィンドウを開きます。

## emacs

`emacs`をエディタとして使用するには、`jrnl`の設定ファイル（`jrnl.yaml`）を以下のように編集します：

```yaml
editor: emacsclient -a "" -c
```

メッセージの編集が終わったら、保存して`C-x #`でバッファを閉じ、emacsclientプロセスを停止します。

## その他のエディタ

他のエディタを使用していて、共有したい場合は、[ドキュメントの貢献](./contributing.md#editing-documentation)を自由に行ってください。
