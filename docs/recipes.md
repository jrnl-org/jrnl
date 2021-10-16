<!-- Copyright (C) 2012-2021 jrnl contributors
     License: https://www.gnu.org/licenses/gpl-3.0.html -->
# FAQ

## Recipes

### Co-occurrence of tags

If I want to find out how often I mentioned my flatmates Alberto and
Melo in the same entry, I run

```sh
jrnl @alberto --tags | grep @melo
```

And will get something like `@melo: 9`, meaning there are 9 entries
where both `@alberto` and `@melo` are tagged. How does this work? First,
`jrnl @alberto` will filter the journal to only entries containing the
tag `@alberto`, and then the `--tags` option will print out how often
each tag occurred in this filtered journal. Finally, we pipe this to
`grep` which will only display the line containing `@melo`.

### Combining filters

You can do things like

```sh
jrnl @fixed -starred -n 10 -to "jan 2013" --short
```

To get a short summary of the 10 most recent, favourite entries before
January 1, 2013 that are tagged with `@fixed`.

### Statistics

How much did I write last year?

```sh
jrnl -from "jan 1 2013" -to "dec 31 2013" | wc -w
```

Will give you the number of words you wrote in 2013. How long is my
average entry?

```sh
expr $(jrnl --export text | wc -w) / $(jrnl --short | wc -l)
```

This will first get the total number of words in the journal and divide
it by the number of entries (this works because `jrnl --short` will
print exactly one line per entry).

### Importing older files

If you want to import a file as an entry to `jrnl`, you can just do `jrnl < entry.ext`. But what if you want the modification date of the file to
be the date of the entry in `jrnl`? Try this

```sh
echo `stat -f %Sm -t '%d %b %Y at %H:%M: ' entry.txt` `cat entry.txt` | jrnl
```

The first part will format the modification date of `entry.txt`, and
then combine it with the contents of the file before piping it to jrnl.
If you do that often, consider creating a function in your `.bashrc` or
`.bash_profile`

```sh
jrnlimport () {
  echo `stat -f %Sm -t '%d %b %Y at %H:%M: ' $1` `cat $1` | jrnl
}
```

### Using templates

!!! note
    Templates require an [external editor](./advanced.md) be configured.

A template is a code snippet that makes it easier to use repeated text
each time a new journal entry is started. There are two ways you can utilize
templates in your entries.

#### 1. Command line arguments

If you had a `template.txt` file with the following contents:

```sh
My Personal Journal
Title:

Body:
```

The `template.txt` file could be used to create a new entry with these
command line arguments:

```sh
jrnl < template.txt     # Imports template.txt as the most recent entry
jrnl -1 --edit          # Opens the most recent entry in the editor
```

#### 2. Include the template file in `jrnl.yaml`

A more efficient way to work with a template file is to declare the file
in your config file by changing the `template` setting from `false` to the
template file's path in double quotes:

```sh
...
template: "/path/to/template.txt"
...
```

Changes can be saved as you continue writing the journal entry and will be
logged as a new entry in the journal you specified in the original argument.

!!! tip
    To read your journal entry or to verify the entry saved, you can use this
    command: `jrnl -n 1` (Check out [Formats](./formats.md) for more options).

```sh
jrnl -n 1
```

### Prompts on shell reload

If you'd like to be prompted each time you refresh your shell, you can include
this in your `.bash_profile`:

```sh
function log_question()
{
   echo $1
   read
   jrnl today: ${1}. $REPLY
}
log_question 'What did I achieve today?'
log_question 'What did I make progress with?'
```

Whenever your shell is reloaded, you will be prompted to answer each of the
questions in the example above. Each answer will be logged as a separate
journal entry at the `default_hour` and `default_minute` listed in your
`jrnl.yaml` [config file](../advanced/#configuration-file).

### Display random entry

You can use this to select one title at random and then display the whole
entry. The invocation of `cut` needs to match the format of the timestamp.
For timestamps that have a space between data and time components, select
fields 1 and 2 as shown. For timestamps that have no whitespace, select
only field 1.

```sh
jrnl -on "$(jrnl --short | shuf -n 1 | cut -d' ' -f1,2)"
```


### Launch a terminal for rapid logging
You can use this to launch a terminal that is the `jrnl` stdin prompt so you can start typing away immediately.

```bash
jrnl now --config-override editor:""
```

Bind this to a keyboard shortcut.

Map `Super+Alt+J` to launch the terminal with `jrnl` prompt

- **xbindkeys**
In your `.xbindkeysrc`

```ini
Mod4+Mod1+j
 alacritty -t floating-jrnl -e jrnl now --config-override editor:"",
```

- **I3 WM** Launch a floating terminal with the `jrnl` prompt

```ini
bindsym Mod4+Mod1+j exec --no-startup-id alacritty -t floating-jrnl -e jrnl --config-override editor:""
for_window[title="floating *"] floating enable
```
### Visualize Formatted Markdown in the CLI

Out of the box, `jrnl` can output journal entries in Markdown. To visualize it, you can pipe to [mdless](https://github.com/ttscoff/mdless), which is a [less](https://en.wikipedia.org/wiki/Less_(Unix))-like tool that allows you to visualize your Markdown text with formatting and syntax highlighting from the CLI. You can use this in any shell that supports piping.

The simplest way to visualize your Markdown output with `mdless` is as follows:
```sh
jrnl --export md | mdless
```

This will render your Markdown output in the whole screen.

Fortunately, `mdless` has an option that allows you to adjust the screen width by using the `-w` option as follows:

```sh
jrnl --export md | mdless -w 70
```

If you want Markdown to be your default display format, you can define this in your config file as follows:

```yaml
display_format: md
# or
display_format: markdown
```

For more information on how `jrnl` outputs your entries in Markdown, please visit the [Formats](./formats.md) section.

## External editors

Configure your preferred external editor by updating the `editor` option
in your `jrnl.yaml` file. (See [advanced usage](./advanced.md) for details).

!!! note
    To save and log any entry edits, save and close the file.

If your editor is not in your operating system's `PATH` environment variable,
then you will have to enter in the full path of your editor.

### Sublime Text

To use [Sublime Text](https://www.sublimetext.com/), install the command line
tools for Sublime Text and configure your `jrnl.yaml` like this:

```yaml
editor: "subl -w"
```

Note the `-w` flag to make sure `jrnl` waits for Sublime Text to close the
file before writing into the journal.

### Visual Studio Code

[Visual Studio Code](https://code.visualstudio.com) also requires a flag
that tells the process to wait until the file is closed before exiting:

```yaml
editor: "code --wait"
```

On Windows, `code` is not added to the path by default, so you'll need to
enter the full path to your `code.exe` file, or add it to the `PATH` variable.

### MacVim

Also similar to Sublime Text, MacVim must be started with a flag that tells
the the process to wait until the file is closed before passing control
back to journal. In the case of MacVim, this is `-f`:

```yaml
editor: "mvim -f"
```

### iA Writer

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

### Notepad++ on Windows

To set [Notepad++](http://notepad-plus-plus.org/) as your editor, edit
the `jrnl` config file (`jrnl.yaml`) like this:

```yaml
editor: "C:\\Program Files (x86)\\Notepad++\\notepad++.exe -multiInst -nosession"
```

The double backslashes are needed so `jrnl` can read the file path
correctly. The `-multiInst -nosession` options will cause `jrnl` to open
its own Notepad++ window.


### emacs

To use `emacs` as your editor, edit the `jrnl` config file (`jrnl.yaml`) like this:

```yaml
editor: emacsclient -a "" -c
```

When you're done editing the message, save and `C-x #` to close the buffer and stop the emacsclient process.
