<!--
Copyright © 2012-2023 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# External editors

Configure your preferred external editor by updating the `editor` option
in your [configuration file](./reference-config-file.md#editor). If your editor is not 
in your operating system's `PATH` environment variable, then you will have to 
enter the full path of your editor.

Once it's configured, you can create an entry as a new document in your editor using the `jrnl` 
command by itself:

``` text
jrnl
```

You can specify the time and title of the entry as usual on the first line of the document. 

If you want, you can skip the editor by including a quick entry with the `jrnl` command:

``` text
jrnl yesterday: All my troubles seemed so far away.
```

If you want to start the entry on the command line and continue writing in your chosen editor, 
use the `--edit` flag. For example:

``` text
jrnl yesterday: All my troubles seemed so far away. --edit
```

!!! note
    To save and log any entry edits, save and close the file.

All editors must be [blocking processes](https://en.wikipedia.org/wiki/Blocking_(computing)) to work with jrnl. Some editors, such as [micro](https://micro-editor.github.io/), are blocking by default, though others can be made to block with additional arguments, such as many of those documented below. If jrnl opens your editor but finishes running immediately, then your editor is not a blocking process, and you may be able to correct that with one of the suggestions below.

Please see [this section](./privacy-and-security.md#editor-history) about how
your editor might leak sensitive information and how to mitigate that risk.

## Sublime Text

To use [Sublime Text](https://www.sublimetext.com/), install the command line
tools for Sublime Text and configure your `jrnl.yaml` like this:

```yaml
editor: "subl -w"
```

Note the `-w` flag to make sure `jrnl` waits for Sublime Text to close the
file before writing into the journal.

## Visual Studio Code

[Visual Studio Code](https://code.visualstudio.com) also requires a flag
that tells the process to wait until the file is closed before exiting:

```yaml
editor: "code --wait"
```

On Windows, `code` is not added to the path by default, so you'll need to
enter the full path to your `code.exe` file, or add it to the `PATH` variable.

## MacVim

Also similar to Sublime Text, MacVim must be started with a flag that tells
the the process to wait until the file is closed before passing control
back to journal. In the case of MacVim, this is `-f`:

```yaml
editor: "mvim -f"
```

## Vim/Neovim

To use any of the Vim derivatives as editor in Linux, simply set the `editor`
to the executable:

```yaml
editor: "vim"
# or
editor: "nvim"
```

## iA Writer

On OS X, you can use the fabulous [iA
Writer](http://www.iawriter.com/mac) to write entries. Configure your
`jrnl.yaml` like this:

```yaml
editor: "open -b pro.writer.mac -Wn"
```

What does this do? `open -b ...` opens a file using the application
identified by the bundle identifier (a unique string for every app out
there). `-Wn` tells the application to wait until it's closed before
passing back control, and to use a new instance of the application.

If the `pro.writer.mac` bundle identifier is not found on your system,
you can find the right string to use by inspecting iA Writer's
`Info.plist` file in your shell:

```sh
grep -A 1 CFBundleIdentifier /Applications/iA\ Writer.app/Contents/Info.plist
```

## Notepad++ on Windows

To set [Notepad++](http://notepad-plus-plus.org/) as your editor, edit
the `jrnl` config file (`jrnl.yaml`) like this:

```yaml
editor: "C:\\Program Files (x86)\\Notepad++\\notepad++.exe -multiInst -nosession"
```

The double backslashes are needed so `jrnl` can read the file path
correctly. The `-multiInst -nosession` options will cause `jrnl` to open
its own Notepad++ window.


## emacs

To use `emacs` as your editor, edit the `jrnl` config file (`jrnl.yaml`) like this:

```yaml
editor: emacsclient -a "" -c
```

When you're done editing the message, save and `C-x #` to close the buffer and stop the emacsclient process.

## Other editors

If you're using another editor and would like to share, feel free to [contribute documentation](./contributing.md#editing-documentation) on it.
