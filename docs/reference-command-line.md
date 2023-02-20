<!--
Copyright © 2012-2023 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# Command Line Reference

## Synopsis
```
usage: jrnl [--debug] [--help] [--version] [--list] [--encrypt] [--decrypt]
            [--import] [-on DATE] [-today-in-history] [-month DATE]
            [-day DATE] [-year DATE] [-from DATE] [-to DATE] [-contains TEXT]
            [-and] [-starred] [-n [NUMBER]] [-not [TAG]] [--edit] [--delete]
            [--format TYPE] [--tags] [--short]
            [--config-override CONFIG_KEY CONFIG_VALUE]
            [--config-file CONFIG_FILE_PATH]
            [[...]]
```

## Standalone Commands

These commands will exit after they complete. You may only run one at a time.

### --help
Show a help message.

### --version
Print version and license information.

### --list
List the config file location, all configured journals, and their locations.

### ---encrypt
Encrypt a journal. See [encryption](encryption.md) for more information.

### --decrypt
Decrypt a journal. See [encryption](encryption.md) for more information.


### --import
Import entries from another journal. If any entries have the exact same content
and timestamp, they will be deduplicated.

Optional parameters:
```sh
--file FILENAME
```
Specify a file to import. If not provided, `jrnl` will use STDIN as the data source.

```sh
--format TYPE
```
Specify the format of the file that is being imported. Defaults to the same data
storage method that jrnl uses. See [formats](formats.md) for more information.

## Writing new entries
See [Basic Usage](usage.md).

## Searching

To find entries from your journal, use any combination of the below filters.
Only entries that match all the filters will be displayed.

When specifying dates, you can use the same kinds of dates you use for new
entries, such as `yesterday`, `today`, `Tuesday`, or `2021-08-01`.

| Search Argument | Description |
| --- | --- |
| -on DATE | Show entries on this date |
| -today-in-history | Show entries of today over the years |
| -month DATE | Show entries on this month of any year |
| -day DATE | Show entries on this day of any month |
| -year DATE | Show entries of a specific year |
| -from DATE | Show entries after, or on, this date |
| -to DATE | Show entries before, or on, this date (alias: -until) |
| -contains TEXT | Show entries containing specific text (put quotes around text with spaces) |
| -and | Show only entries that match all conditions, like saying "x AND y" (default: OR) |
| -starred | Show only starred entries (marked with *) |
| -tagged | Show only tagged entries (marked with the [configured tagsymbols](reference-config-file.md#tagsymbols)) |
| -n [NUMBER] | Show a maximum of NUMBER entries (note: '-n 3' and '-3' have the same effect) |
| -not [TAG] | Exclude entries with this tag |
| -not -starred | Exclude entries that are starred |
| -not -tagged | Exclude entries that are tagged |

## Searching Options
These help you do various tasks with the selected entries from your search.
If used on their own (with no search), they will act on your entire journal.

### --edit
Opens the selected entries in your configured editor. It will fail if the
`editor` key is not set in your config file.

Once you begin editing, you can add multiple entries and delete entries
by modifying the text in your editor. When your editor closes, jrnl reads
the temporary file you were editing and makes the changes to your journal.

### --delete
Interactively deletes selected entries. You'll be asked to confirm deletion of
each entry.

### --change-time DATE
Interactively changes the time of the selected entries to the date specified,
or to right now if no date is specified. You'll be asked to confirm each entry,
unless you are using this with `--edit` on a single entry.

### --format TYPE
Display selected entries in an alternate format. See [formats](formats.md).

#### Optional parameters
```sh
--file FILENAME
```
Write output to file instead of STDOUT. In most shells, the
same effect can be achieved using `>`.

### --tags

Alias for '--format tags'. Returns a list of all tags and the number of times
they occur within the searched entries. If there are no tags found, `jrnl` will output a message saying so.

### --short
Only shows the date and titles of the searched entries.

## Configuration arguments

### --config-override CONFIG_KEY CONFIG_VALUE

Override configured key-value pair with CONFIG_KV_PAIR for this command invocation only. To access config keys that aren't at the top level, separate the keys with a dot, such as `colors.title` to access the `title` key within the `colors` key. Read [advanced usage](./advanced.md) for examples.

### --config-file CONFIG_FILE_PATH

Use the config file at CONFIG_FILE_PATH for this command invocation only.
Read [advanced usage](./advanced.md) for examples.

## Other Arguments

### --debug
Prints information useful for troubleshooting while `jrnl` executes.

### --diagnostic
Prints diagnostic information useful for [reporting issues](https://github.com/jrnl-org/jrnl/issues).