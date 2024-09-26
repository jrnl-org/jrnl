<!--
Copyright © 2012-2023 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# ヒントとコツ

このページでは、他のツールや外部エディタと組み合わせて
jrnlを使用するためのヒントとコツを紹介します。

## Co-occurrence of tags

ルームメイトの AlbertoとMeloを同じエントリーでどれくらい一緒に言及したか調べたい場合、
次のコマンドを使います。

```sh
jrnl @alberto --tags | grep @melo
```

これにより、`@melo: 9`と言った結果が表示されます。これは`@alberto`と
`@melo`の両方がタグ付けされたエントリーが9件あることを意味しています。
仕組みを説明すると､まず`jrnl @alberto` が`@alberto`タグの有るエントリーだけを
抽出します。次に `--tags`オプションを使うと、その抽出されたエントリー内で
各タグがどれくらい使われているかが表示されます。最後に、`grep`で`@melo`を
含み行だけを示しています。

## フィルターの組み合わせ

次のようにコマンドを使うことが出来ます。

```sh
jrnl @fixed -starred -n 10 -to "jan 2013" --short
```

これで2013年1月1日以前に`@fixed`タグが付けられた最近のお気に入りの10件の
エントリーの要約を取得できます。

## 統計

昨年どれくらい書いたか知りたい場合は？

```sh
jrnl -from "jan 1 2013" -to "dec 31 2013" | wc -w
```

このコマンドを実行すると、2013年に書いた単語数が表示されます。

エントリーの平均の長さを知りたい場合は？

```sh
expr $(jrnl --export text | wc -w) / $(jrnl --short | wc -l)
```

このコマンドは、まずジャーナル全体の単語数を取得し､それをエントリーの数で
割ります(`jrnl --short`は各エントリーごとに1行だけ出力するため、この方法が機能
します)。

## 古いファイルのインポート

ファイルを `jrnl` のエントリとしてインポートしたい場合は、
単に `jrnl < entry.ext` と実行するだけです。
しかし、ファイルの最終更新日時を `jrnl` のエントリの日付として設定したい場合はどうでしょうか？

次のコマンドを試してみてください。

```sh
echo `stat -f %Sm -t '%d %b %Y at %H:%M: ' entry.txt` `cat entry.txt` | jrnl
```

このコマンドの前半部分は `entry.txt` の最終更新日時をフォーマットし、ファイルの内容と結合してからそれを `jrnl` にパイプします。これを頻繁に行う場合は、`.bashrc` や `.bash_profile` に関数を作成することを検討してください。

```sh
jrnlimport () {
  echo `stat -f %Sm -t '%d %b %Y at %H:%M: ' $1` `cat $1` | jrnl
}
```

## テンプレートの使用

!!! 注意
テンプレートを使用するには、[外部エディタ](./advanced.md) の設定が必要です。

テンプレートは、構造化されたジャーナルを作成するために使うテキストファイルです。テンプレートを使用する方法は3つあります。

### 1. `--template` コマンドライン引数とデフォルトの `$XDG_DATA_HOME/jrnl/templates` ディレクトリを使用

`$XDG_DATA_HOME/jrnl/templates` は、テンプレートを保存するためにデフォルトで作成されます！このディレクトリにテンプレート（例えば `default.md`）を作成し、`--template FILE_IN_DIR` として指定します。

```sh
jrnl --template default.md
```

### 2. `--template` コマンドライン引数とローカル/絶対パスを使用

任意のテキストでテンプレートファイルを作成できます。例は以下の通りです：

```sh
# /tmp/template.txt
私の個人ジャーナル
タイトル：

本文：
```

その後、テンプレートファイルの絶対パスまたは相対パスを引数として指定すると、外部エディタが開き、テンプレートが事前に入力された状態になります。

```sh
jrnl --template /tmp/template.md
```

### 3. `jrnl.yaml` にデフォルトのテンプレートファイルを設定

デフォルトでテンプレートを使用したい場合は、[設定ファイル](./reference-config-file.md) 内の `template` の値を `false` からダブルクオーテーションで囲まれたテンプレートファイルのパスに変更します。

```sh
...
template: "/path/to/template.txt"
...
```

!!! ヒント
ジャーナルエントリを確認したり、保存されたエントリを確認したい場合は、以下のコマンドを使用します：`jrnl -n 1` （他のオプションについては[フォーマット](./formats.md) を確認してください）。

```sh
jrnl -n 1
```

## シェルのリロード時にプロンプトを表示

シェルをリフレッシュするたびにプロンプトを表示させたい場合は、以下を `.bash_profile` に追加できます：

```sh
function log_question()
{
   echo $1
   read
   jrnl today: ${1}. $REPLY
}
log_question '今日達成したことは何ですか？'
log_question 'どんな進展がありましたか？'
```

シェルがリロードされるたびに、上記の質問に回答するように促されます。各回答は、`jrnl.yaml` の `default_hour` および `default_minute` にリストされている時刻で別々のジャーナルエントリとして記録されます。

## ランダムエントリの表示

ランダムに1つのタイトルを選択し、エントリ全体を表示することができます。タイムスタンプのフォーマットに合わせて `cut` の呼び出しを調整します。日時要素の間にスペースがあるタイムスタンプでは、以下のようにフィールド1と2を選択します。スペースがないタイムスタンプの場合は、フィールド1のみを選択します。

```sh
jrnl -on "$(jrnl --short | shuf -n 1 | cut -d' ' -f1,2)"
```

## 高速記録用の端末を起動

`jrnl` の stdin プロンプトを持つ端末を起動し、すぐに入力を開始できるようにすることができます。

```bash
jrnl --config-override editor ""
```

これをキーボードショートカットに割り当てます。

`Super+Alt+J` に `jrnl` プロンプトを持つ端末を起動するようにマップする

- **xbindkeys**
  あなたの `.xbindkeysrc` に以下を追加します

```ini
Mod4+Mod1+j
 alacritty -t floating-jrnl -e jrnl --config-override editor "",
```

- **I3 WM** `jrnl` プロンプトを持つフローティング端末を起動します

```ini
bindsym Mod4+Mod1+j exec --no-startup-id alacritty -t floating-jrnl -e jrnl --config-override editor ""
for_window[title="floating *"] floating enable
```

## CLI でフォーマットされた Markdown を視覚化

`jrnl` はデフォルトでジャーナルエントリをMarkdown形式で出力できます。これを視覚化するには、[mdless](https://github.com/ttscoff/mdless) にパイプします。`mdless` は、Markdownテキストをフォーマットおよびシンタックスハイライト付きでCLIで表示できる、[less](<https://en.wikipedia.org/wiki/Less_(Unix)>) のようなツールです。この機能は、パイプをサポートする任意のシェルで使用できます。

Markdown出力を `mdless` で視覚化する最も簡単な方法は次の通りです：

```sh
jrnl --export md | mdless
```

これにより、画面全体にMarkdown出力がレンダリングされます。

幸いなことに、`mdless` には画面幅を調整するための `-w` オプションがあります。以下のように使用します：

```sh
jrnl --export md | mdless -w 70
```

Markdownをデフォルトの表示形式にしたい場合は、設定ファイルで次のように定義できます：

```yaml
display_format: md
# または
display_format: markdown
```

`jrnl` がエントリをMarkdown形式で出力する方法についての詳細は、[フォーマット](./formats.md) セクションを参照してください。

## バッファの末尾にジャンプ（vi使用時）

viを使用して編集する際に、エントリの最後の行にジャンプさせるには、設定ファイルで次のように設定します：

```yaml
editor: vi + -c "call cursor('.',strwidth(getline('.')))"
```
