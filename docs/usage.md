# Basic Usage

`jrnl` has two modes: **composing** and **viewing**. Whenever you don't enter
any arguments that start with a dash (`-`) or double-dash (`--`), you're in
composing mode, meaning that you can write your entry on the command line.

We intentionally break a convention on command line arguments: all arguments
starting with a _single dash_ (`-`) will _filter_ your journal before viewing
it. Filter arguments can be combined arbitrarily. Arguments with a _double dash_
(`--`) will _control_ how your journal is displayed or exported. Control
arguments are mutually exclusive (i.e., you can only specify one way to display
or export your journal at a time).

## Listing Journals

You can list the journals accessible by `jrnl`:

```sh
jrnl -ls
```

The journals displayed correspond to those specified in the `jrnl` configuration
file.

## Composing Entries

Composing mode is entered by either starting `jrnl` without any arguments --
which will prompt you to write an entry or launch your editor -- or by just
writing an entry on the prompt, such as

```sh
jrnl today at 3am: I just met Steve Buscemi in a bar! He was on fire.
```

!!! note
    Most shells contain a certain number of reserved characters, such as `#` and
    `*`. These characters, as well as unbalanced single or double quotation
    marks, parentheses, and others, likely will cause problems. Although
    reserved characters can be escaped using `\`, this is not ideal for
    long-form writing. The solution: first enter `jrnl` and hit `return`. You
    can then enter the text of your journal entry. Alternatively, you can `use
    an external editor <advanced>`).

You can also import an entry directly from a file

```sh
jrnl < my_entry.txt
```

### Smart timestamps

Timestamps that work:

- at 6am
- yesterday
- last monday
- sunday at noon
- 2 march 2012
- 7 apr
- 5/20/1998 at 23:42

### Starring entries

To mark an entry as a favorite, simply "star" it

```sh
jrnl last sunday *: Best day of my life.
```

If you don't want to add a date (i.e., you want the date to be entered as
_now_), the following options are equivalent:

- `jrnl *: Best day of my life.`
- `jrnl *Best day of my life.`
- `jrnl Best day of my life.*`

!!! note
    Make sure that the asterisk sign is **not** surrounded by whitespaces. `jrnl
    Best day of my life! *` will not work because the `*` sign has a special
    meaning in most shells).

## Viewing

```sh
jrnl -n 10
```

lists the ten most recent entries (`jrnl -10` works the same way).

```sh
jrnl -from "last year" -until march
```

displays everything that happened from the beginning of last year until the
beginning of the past March. To display only your favorite (starred) entries,
use

```sh
jrnl -starred
```

## Using Tags

Keep track of people, projects or locations, by tagging them with an `@`
in your entries:

```sh
jrnl Had a wonderful day at the @beach with @Tom and @Anna.
```

You can filter your journal entries by tag. For example,

```sh
jrnl @pinkie @WorldDomination
```

displays all entries in which either `@pinkie` or `@WorldDomination`
occurred.

```sh
jrnl -n 5 -and @pinkie @WorldDomination
```

displays the last five entries containing both `@pinkie` **and**
`@worldDomination`. You can change which symbols you'd like to use for tagging
in the configuration.

!!! note
    Entering `jrnl @pinkie @WorldDomination` will display entries in which both
    tags are present because, although no command line arguments are given, all
    of the input strings look like tags. `jrnl` will assume you want to filter
    by tag, rather than create a new entry that consists only of tags.


## Editing Existing Entries

You can edit entries after writing them. This is particularly useful when your
journal file is encrypted. To use this feature, you need to have an external
editor configured in your configuration file (see `advanced usage <advanced>`).
You can also edit only the entries that match specific search criteria. For
example,

```sh
jrnl -until 1950 @texas -and @history --edit
```

opens your external editor displaying all entries tagged with `@texas` and
`@history` that were written before 1950. After making changes, save and close
the file, and only those entries will be modified (and encrypted, if
applicable).

If you are using multiple journals, it's easy to edit specific entries from
specific journals. Simply prefix the filter string with the name of the journal.
For example,

```sh
jrnl work -n 1 --edit
```

opens the most recent entry in the 'work' journal in your external editor.

You can also use this feature for deleting entries from your journal. Open an external editor with the entries you want to delete...

```sh
jrnl @texas -until 'june 2012' --edit
```

...select all text, delete it, save and close, and all of those entries are
removed from the journal.
