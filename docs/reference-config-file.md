<!--
Copyright © 2012-2022 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# Configuration File Reference

`jrnl` stores its information in a YAML configuration file.

!!! note
    Backup your journal and config file before editing. Changes to the config file
    can have destructive effects on your journal!

## Config location
You can find your configuration file location by running:
`jrnl --list`

By default, the configuration file is `~/.config/jrnl/jrnl.yaml`.
If you have the `XDG_CONFIG_HOME` variable set, the configuration
file will be saved as `$XDG_CONFIG_HOME/jrnl/jrnl.yaml`.

!!! note
    On Windows, the configuration file is typically found at
    `%USERPROFILE%\.config\jrnl\jrnl.yaml`.


## Config format
The configuration file is a [YAML](https://yaml.org/) file and can be edited with
a text editor.

## Config keys

### journals

Describes each journal used by `jrnl`. Each indented key after this key is
the name of a journal.

If a journal key has a value, that value will be interpreted as the path
to the journal. Otherwise, the journal needs the additional indented key
`journal` to specify its path.

All keys below can be specified for each journal at the same level as the
`journal` key. If a key conflicts with a top-level key, the journal-specific
key will be used instead.

### editor
If set, executes this command to launch an external editor for
writing and editing your entries. The path to a temporary file
is passed after it, and `jrnl` processes the file once
the editor is closed.

Some editors require special options to work properly. See
[External Editors](external-editors.md) for details.

### encrypt
If `true`, encrypts your journal using AES. Do not change this
value for journals that already have data in them.

### template
The path to a text file to use as a template for new entries. Only works when you
have the `editor` field configured.

### tagsymbols
Symbols to be interpreted as tags.

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

### default_hour and default_minute
Entries will be created at this time if you supply a date but no specific time (for example, `last thursday`).

### timeformat
Defines how to format the timestamps as they are stored in your journal.
See the [python docs](http://docs.python.org/library/time.html#time.strftime) for reference.

Do not change this for an existing journal, since that might lead
to data loss.

If you would just like to change how `jrnl` displays dates,
use display_format instead.

!!! note
    `jrnl` doesn't support the `%z` or `%Z` time zone identifiers.

### highlight
If `true`, tags will be highlighted in cyan.

### linewrap
Controls the width of the output. Set to `false` if you don't want to
wrap long lines. Set to `auto` to let `jrnl` automatically determine
the terminal width.

### colors
A dictionary that controls the colors used to display journal entries.
It has four subkeys, which are: `body`, `date`, `tags`, and `title`.

Current valid values are: `BLACK`, `RED`, `GREEN`, `YELLOW`, `BLUE`,
`MAGENTA`, `CYAN`, `WHITE`, and `NONE`.

`colorama.Fore` is used for colorization, and you can find the [docs here](https://github.com/tartley/colorama#colored-output).

To disable colored output, set the value to `NONE`.

### display_format
Specifies formatter to use by default. See [formats](formats.md).

### version
`jrnl` automatically updates this field to the version that it is running.
There is no need to change this field manually.
