# Basic Usage

`jrnl` has two modes: **composing** and **viewing**. Basically, whenever
you _don't_ supply any arguments that start
with a dash or double-dash, you're in composing mode, meaning you can
write your entry on the command line or an editor of your choice.

We intentionally break a convention on command line arguments: all
arguments starting with a _single dash_
will _filter_ your journal before viewing
it, and can be combined arbitrarily. Arguments with a
_double dash_ will control how your journal
is displayed or exported and are mutually exclusive (ie. you can only
specify one way to display or export your journal at a time).

## Listing Journals

You can list the journals accessible by jrnl

```sh
jrnl -ls
```

The journals displayed correspond to those specified in the jrnl
configuration file.

## Composing Entries

Composing mode is entered by either starting `jrnl` without any
arguments -- which will prompt you to write an entry or launch your
editor -- or by just writing an entry on the prompt, such as

```sh
jrnl today at 3am: I just met Steve Buscemi in a bar! He looked funny.
```

!!! note
Most shell contains a certain number of reserved characters, such as `#`
and `*`. Unbalanced quotes, parenthesis, and so on will also get into
the way of your editing.
For writing longer entries, just enter `jrnl`
and hit `return`. Only then enter the text of your journal entry.
Alternatively, `use an external editor <advanced>`).

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

To mark an entry as a favourite, simply "star" it

```sh
jrnl last sunday *: Best day of my life.
```

If you don't want to add a date (ie. your entry will be dated as now),
The following options are equivalent:

- `jrnl *: Best day of my life.`
- `jrnl *Best day of my life.`
- `jrnl Best day of my life.*`

!!! note
Just make sure that the asterisk sign is **not** surrounded by
whitespaces, e.g. `jrnl Best day of my life! *` will **not** work (the
reason being that the `*` sign has a special meaning on most shells).

## Viewing

```sh
jrnl -n 10
```

will list you the ten latest entries (if you're lazy, `jrnl -10` will do
the same),

```sh
jrnl -from "last year" -until march
```

everything that happened from the start of last year to the start of
last march. To only see your favourite entries, use

```sh
jrnl -starred
```

## Using Tags

Keep track of people, projects or locations, by tagging them with an `@`
in your entries

```sh
jrnl Had a wonderful day on the @beach with @Tom and @Anna.
```

You can filter your journal entries just like this:

```sh
jrnl @pinkie @WorldDomination
```

Will print all entries in which either `@pinkie` or `@WorldDomination`
occurred.

```sh
jrnl -n 5 -and @pineapple @lubricant
```

the last five entries containing both `@pineapple` **and** `@lubricant`.
You can change which symbols you'd like to use for tagging in the
configuration.

!!! note
`jrnl @pinkie @WorldDomination` will switch to viewing mode because
although **no** command line arguments are given, all the input strings
look like tags - _jrnl_ will assume you want to filter by tag.

## Editing older entries

You can edit selected entries after you wrote them. This is particularly
useful when your journal file is encrypted. To use this feature, you need
to have an editor configured in your journal configuration file (see
`advanced usage <advanced>`)

```sh
jrnl -until 1950 @texas -and @history --edit
```

Will open your editor with all entries tagged with `@texas` and
`@history` before 1950. You can make any changes to them you want; after
you save the file and close the editor, your journal will be updated.

Of course, if you are using multiple journals, you can also edit e.g.
the latest entry of your work journal with `jrnl work -n 1 --edit`. In
any case, this will bring up your editor and save (and, if applicable,
encrypt) your edited journal after you save and exit the editor.

You can also use this feature for deleting entries from your journal

```sh
jrnl @girlfriend -until 'june 2012' --edit
```

Just select all text, press delete, and everything is gone...
