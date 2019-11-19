# Advanced Usage

## Configuration File

You can configure the way jrnl behaves in a configuration file. By
default, this is `~/.config/jrnl/jrnl.yaml`. If you have the `XDG_CONFIG_HOME`
variable set, the configuration file will be saved as
`$XDG_CONFIG_HOME/jrnl/jrnl.yaml`.

!!! note
    On Windows, the configuration file is typically found at `%USERPROFILE%\.config\jrnl\jrnl.yaml`.

The configuration file is a YAML file with the following options
and can be edited with a plain text editor.

!!! note
    Backup your config file before editing. Changes to the config file
    have destructive effects on your journal!

  - `journals`
    paths to your journal files
  - `editor`
    if set, executes this command to launch an external editor for
    writing your entries, e.g. `vim`. Some editors require special
    options to work properly, see `FAQ <recipes>` for details.
  - `encrypt`
    if `true`, encrypts your journal using AES.
  - `tagsymbols`
    Symbols to be interpreted as tags. (See note below)
  - `default_hour` and `default_minute`
    if you supply a date, such as `last thursday`, but no specific
    time, the entry will be created at this time
  - `timeformat`
    how to format the timestamps in your journal, see the [python docs](http://docs.python.org/library/time.html#time.strftime) for reference
  - `highlight`
    if `true`, tags will be highlighted in cyan.
  - `linewrap`
    controls the width of the output. Set to `false` if you don't want to wrap long lines.
  - `colors`
    dictionary that controls the colors used to display journal entries. It has two subkeys, which are: `date` and `title`. Current valid values are: `BLACK`, `RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, and `WHITE`. `colorama.Fore` is used for colorization, and you can find the [docs here](https://github.com/tartley/colorama#colored-output). To disable colored output, set the value to `NONE`. If you set the value of any color subkey to an invalid color, no color will be used.

!!! note
    Although it seems intuitive to use the `#`
    character for tags, there's a drawback: on most shells, this is
    interpreted as a meta-character starting a comment. This means that if
    you type

    > `jrnl Implemented endless scrolling on the #frontend of our website.`

    your bash will chop off everything after the `#` before passing it to
      `jrnl`. To avoid this, wrap your input into quotation marks like
      this:

    > `jrnl "Implemented endless scrolling on the #frontend of our website."`

  Or use the built-in prompt or an external editor to compose your
  entries.

## Multiple journal files

You can configure `jrnl`to use with multiple journals (eg.
`private` and `work`) by defining more journals in your `jrnl.yaml`,
for example:

``` yaml
journals:
  default: ~\journal.txt
  work: ~\work.txt
```

The `default` journal gets created the first time you start `jrnl`
Now you can access the `work` journal by using `jrnl work` instead of
`jrnl`, eg.

``` sh
jrnl work at 10am: Meeting with @Steve
jrnl work -n 3
```

will both use `~/work.txt`, while `jrnl -n 3` will display the last
three entries from `~/journal.txt` (and so does `jrnl default -n 3`).

You can also override the default options for each individual journal.
If your `jrnl.yaml` looks like this:

``` yaml
encrypt: false
journals:
default: ~/journal.txt
work:
  journal: ~/work.txt
  encrypt: true
food: ~/my_recipes.txt
```

Your `default` and your `food` journals won't be encrypted, however your
`work` journal will! You can override all options that are present at
the top level of `jrnl.yaml`, just make sure that at the very least
you specify a `journal: ...` key that points to the journal file of
that journal.

!!! note
    Changing `encrypt` to a different value will not encrypt or decrypt your
    journal file, it merely says whether or not your journal
    is encrypted. Hence manually changing
    this option will most likely result in your journal file being
    impossible to load.

## Known Issues

### Unicode on Windows

The Windows shell prior to Windows 7 has issues with unicode encoding.
To use non-ascii characters, first tweak Python to recognize the encoding by adding `'cp65001': 'utf_8'`, to `Lib/encoding/aliases.py`. Then, change the codepage with `chcp 1252` before using `jrnl`.

(Related issue: [#486](https://github.com/jrnl-org/jrnl/issues/486))
