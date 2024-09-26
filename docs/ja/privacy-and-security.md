<!--
Copyright © 2012-2023 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# プライバシーとセキュリティ

`jrnl`はプライバシーとセキュリティを念頭に置いて設計されていますが、他のプログラムと同様に、
注意すべきいくつかの制限があります。

## パスワードの強度

`jrnl`はパスワードの強度要件を強制しません。短いまたは一般的に使用されるパスワードは、
基本的なセキュリティスキルを持つ人が暗号化された`jrnl`ファイルにアクセスするのを
簡単に回避できてしまいます。

## 合理的否認

ジャーナルの内容を暗号化の層の背後に隠すことはできますが、誰かがあなたの設定ファイルに
アクセスできる場合、ジャーナルの存在、そのジャーナルファイルの場所、最後に編集した
時期を知ることができます。十分な力の不均衡がある場合、誰かが非技術的な手段を通じて
あなたに暗号化を解除させることができるかもしれません。

## スパイ行為

`jrnl`は開かれていない間のジャーナルエントリーへの不正アクセスから保護できますが、
安全でないコンピューター/場所からは保護できません。例えば：

- 誰かがキーロガーをインストールし、ジャーナルに入力する内容を追跡する。
- 誰かがエントリーを書いている間にあなたの画面を見ている。
- 誰かが`jrnl`にバックドアをインストールしたり、ジャーナルを毒して
  エントリーを明らかにするよう仕向けたりする。

## 保存されたパスワード

暗号化されたジャーナルを作成する際、「パスワードをキーチェーンに保存するか」と
尋ねられます。このキーチェーンは[Python keyringライブラリ](https://pypi.org/project/keyring/)を
使用してアクセスされ、オペレーティングシステムによって動作が異なります。

Windowsでは、キーチェーンはWindows Credential Manager（WCM）で、ロックできず、
あなたのユーザー名で実行されている他のアプリケーションからアクセスできます。
これが心配な場合は、パスワードを保存しないほうがよいかもしれません。

## シェル履歴

コマンドラインからエントリーを入力できるため、コマンドライン操作をログに記録する
ツールは潜在的なセキュリティリスクとなります。以下に、様々なシェルでこの問題に
対処する方法を示します。

### bash

`~/.bashrc`ファイルに以下の行を追加することで、jrnlの履歴ログを無効にできます：

```sh
HISTIGNORE="$HISTIGNORE:jrnl *"
```

`bash`履歴から既存の`jrnl`コマンドを削除するには、bashの履歴ファイルから
単純に削除します。このファイルのデフォルトの場所は`~/.bash_history`ですが、
必要に応じて`echo "$HISTFILE"`を実行して見つけることができます。また、
`history -c`を実行して履歴からすべてのコマンドを削除することもできます。

### zsh

`~/.zshrc`ファイルに以下を追加することで、jrnlの履歴ログを無効にできます：

```sh
setopt HIST_IGNORE_SPACE
alias jrnl=" jrnl"
```

`zsh`履歴から既存の`jrnl`コマンドを削除するには、zshの履歴ファイルから
単純に削除します。このファイルのデフォルトの場所は`~/.zsh_history`ですが、
必要に応じて`echo "$HISTFILE"`を実行して見つけることができます。また、
`history -c`を実行して履歴からすべてのコマンドを削除することもできます。

### fish

デフォルトでは、`fish`はスペースで始まるコマンドをログに記録しません。
常にjrnlの前にスペースを付けて実行したい場合は、`~/.config/fish/config.fish`
ファイルに以下を追加できます：

```sh
abbr --add jrnl " jrnl"
```

`fish`履歴から既存のjrnlコマンドを削除するには、`history delete --prefix 'jrnl '`を実行します。

### Windowsコマンドプロンプト

Windowsは履歴をディスクにログ記録しませんが、コマンドプロンプトセッションには
保持されます。ジャーナリング後、コマンドプロンプトを閉じるか`Alt`+`F7`を
押して履歴をクリアしてください。

## エディターからjrnlへの転送中のファイル

エントリーの作成や編集時、`jrnl`はエディターがジャーナルにアクセスできるよう
ディスク上に暗号化されていない一時ファイルを使用します。エディターを閉じた後、
`jrnl`はこの一時ファイルを削除します。

つまり、ジャーナルエントリーを保存したがまだエディターを閉じていない場合、
暗号化されていない一時ファイルがディスク上に残ります。この間にコンピューターが
シャットダウンしたり、`jrnl`プロセスが予期せず終了したりすると、暗号化されて
いない一時ファイルがディスク上に残ります。この問題を軽減するには、エディターを
閉じる直前にのみ保存するようにしてください。また、一時フォルダからこれらの
ファイルを手動で削除することもできます。デフォルトでは、これらは`jrnl*.jrnl`
という名前ですが、[テンプレート](reference-config-file.md#template)を使用して
いる場合は、テンプレートと同じ拡張子になります。

## エディター履歴

一部のエディターは、将来の使用のためにディスク上に使用履歴を保存します。
これは、最近の検索パターンやエディターコマンドを通じて機密情報が漏洩する
可能性があるという意味でセキュリティリスクとなる可能性があります。

### Visual Studio Code

Visual Studio Codeは、後でコンテンツを復元またはレビューできるように、
保存されたファイルの内容を保存します。すべてのファイルに対してこの機能を
無効にするには、[設定エディター](https://code.visualstudio.com/docs/getstarted/settings#_settings-editor)で
`workbench.localHistory.enabled`設定のチェックを外します。

または、`workbench.localHistory.exclude`設定で[パターン](https://code.visualstudio.com/docs/editor/codebasics#_advanced-search-options)を
設定することで、特定のファイルに対してこの機能を無効にできます。`jrnl`によって
生成される暗号化されていない一時ファイルを除外するには、[設定エディター](https://code.visualstudio.com/docs/getstarted/settings#_settings-editor)で
`workbench.localHistory.exclude`設定に`**/jrnl*.jrnl`パターンを設定できます
（[テンプレート](reference-config-file.md#template)を使用していない場合）。

!!! note
Windowsでは、履歴の場所は通常`%APPDATA%\Code\User\History`にあります。

Visual Studio Codeは、開いているすべての未保存ファイルのコピーも作成します。
これらのコピーはバックアップ場所に保存され、ファイルを保存すると自動的に
クリーンアップされます。ただし、ファイルを保存する前にコンピューターが
シャットダウンしたり、Visual Studio Codeプロセスが予期せず停止したりすると、
暗号化されていない一時ファイルがディスク上に残る可能性があります。これらの
ファイルはバックアップ場所から手動で削除できます。

!!! note
Windowsでは、バックアップ場所は通常`%APPDATA%\Code\Backups`にあります。

### Vim

Vimは`~/.viminfo`にある所謂Viminfoファイルに進捗データを保存します。
これにはコマンドライン履歴、検索文字列履歴、検索/置換パターン、レジスタの
内容など、あらゆる種類のユーザーデータが含まれています。また、予期せぬ
アプリケーションの終了後に開いていたファイルを復元できるよう、Vimはスワップ
ファイルを使用します。

これらのオプションや他の情報漏洩の可能性のある機能は、Jrnl設定の`editor`キーを
以下のように設定することで無効にできます：

```yaml
editor: "vim -c 'set viminfo= noswapfile noundofile nobackup nowritebackup noshelltemp history=0 nomodeline secure'"
```

すべてのプラグインとカスタム設定を無効にし、デフォルト設定でVimを起動するには、
コマンドラインで`-u NONE`を渡すこともできます。これにより、悪意のあるプラグインや
その他の検出が困難な情報漏洩が確実に排除されます。ただし、これによりエディター
の使用感が大幅に低下します。

代わりに、Jrnlファイルが編集されているときに自動的に検出するようVimに設定するには、
autocommandを使用できます。これを`~/.vimrc`に配置します：

```vim
autocmd BufNewFile,BufReadPre *.jrnl setlocal viminfo= noswapfile noundofile nobackup nowritebackup noshelltemp history=0 nomodeline secure
```

!!! note
[テンプレート](reference-config-file.md#template)を使用している場合は、
`.jrnl`の代わりにテンプレートのファイル拡張子を使用する必要があります。

言及したオプションの詳細については、Vimで`:h <option>`を参照してください。

### Neovim

Neovimは主にVimと互換性があるよう努めており、そのためVimと同様の機能を
持っています。Neovimの1つの違いは、Viminfoファイルの代わりにShaDa
（"shared data"）ファイルと呼ばれるものが`~/.local/state/nvim`
（Neovim v0.8.0以前は`~/.local/share/nvim`）にあることです。ShaDaファイルは
Vimと同じ方法で無効にできます。

```yaml
editor: "nvim -c 'set shada= noswapfile noundofile nobackup nowritebackup noshelltemp history=0 nomodeline secure'"
```

ここでも`-u NONE`を渡して、デフォルト設定でセッションを開始できます。

上記のVimと同様に、Vimscriptでautocommandを作成できます：

```vim
autocmd BufNewFile,BufReadPre *.jrnl setlocal shada= noswapfile noundofile nobackup nowritebackup noshelltemp history=0 nomodeline secure
```

または、同じことをLuaで：

```lua
vim.api.nvim_create_autocmd( {"BufNewFile","BufReadPre" }, {
  group = vim.api.nvim_create_augroup("PrivateJrnl", {}),
  pattern = "*.jrnl",
  callback = function()
    vim.o.shada = ""
    vim.o.swapfile = false
    vim.o.undofile = false
    vim.o.backup = false
    vim.o.writebackup = false
    vim.o.shelltemp = false
    vim.o.history = 0
    vim.o.modeline = false
    vim.o.secure = true
  end,
})
```

!!! note
[テンプレート](reference-config-file.md#template)を使用している場合は、
`.jrnl`の代わりにテンプレートのファイル拡張子を使用する必要があります。

言及したオプションの詳細については、Neovimで`:h <option>`を参照してください。

## 他のリスクに気づいた場合

[GitHubで問題を提出](https://github.com/jrnl-org/jrnl/issues)して、メンテナーに知らせてください。
