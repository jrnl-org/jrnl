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
jrnl @fixed -starred -n 10 -until "jan 2013" --short
```

To get a short summary of the 10 most recent, favourited entries before
January 1, 2013 that are tagged with `@fixed`.

### Statistics

How much did I write last year?

```sh
jrnl -from "jan 1 2013" -until "dec 31 2013" | wc -w
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

If you want to import a file as an entry to jrnl, you can just do `jrnl < entry.ext`. But what if you want the modification date of the file to
be the date of the entry in jrnl? Try this

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
command line arguements:

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
    command: `jrnl -n 1` (Check out [Import and Export](./export.md) for more export options).

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

## External editors

Configure your preferred external editor by updating the `editor` option 
in your `jrnl.yaml` file. (See [advanced usage](./advanced.md) for details). 

!!! note
    To save and log any entry edits, save and close the file.

### Sublime Text

To use Sublime Text, install the command line tools for Sublime Text and
configure your `jrnl.yaml` like this:

```yaml
editor: "subl -w"
```

Note the `-w` flag to make sure jrnl waits for Sublime Text to close the
file before writing into the journal.

### MacVim

Similar to Sublime Text, MacVim must be started with a flag that tells
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
the jrnl config file (`jrnl.yaml`) like this:

```yaml
editor: "C:\\Program Files (x86)\\Notepad++\\notepad++.exe -multiInst -nosession"
```

The double backslashes are needed so jrnl can read the file path
correctly. The `-multiInst -nosession` options will cause jrnl to open
its own Notepad++ window.

### Visual Studio Code

To set [Visual Studo Code](https://code.visualstudio.com) as your editor on Linux, edit `jrnl.yaml` like this:

```yaml
editor: "/usr/bin/code --wait"
```

The `--wait` argument tells VS Code to wait for files to be written out before handing back control to jrnl.

On MacOS you will need to add VS Code to your PATH. You can do that by adding:

```sh
export PATH="\$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"
```

to your `.bash_profile`, or by running the **Install 'code' command in PATH** command from the command pallet in VS Code.

Then you can add:

```yaml
editor: "code --wait"
```

to `jrnl.yaml`. See also the [Visual Studio Code documentation](https://code.visualstudio.com/docs/setup/mac)
