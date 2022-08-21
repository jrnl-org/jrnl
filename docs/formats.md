<!--
Copyright © 2012-2022 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# Formats

`jrnl` supports a variety of alternate formats. These can be used to display your
journal in a different manner than the `jrnl` default, and can even be used to pipe data
from your journal for use in another program to create reports, or do whatever you want
with your `jrnl` data.

Any of these formats can be used with a search (e.g. `jrnl -contains "lorem ipsum"
--format json`) to display the results of that search in the given format, or can be
used alone (e.g. `jrnl --format json`) to display all entries from the selected journal.

This page shows examples of all the built-in formats, but since `jrnl` supports adding
more formats through plugins, you may have more available on your system. Please see
`jrnl --help` for a list of which formats are available on your system.

Any of these formats can be used interchangeably, and are only grouped into "display",
"data", and "report" formats below for convenience.

## Display Formats
These formats are mainly intended for displaying your journal in the terminal. Even so,
they can still be used in the same way as any other format (like written to a file, if
you choose).

### Pretty
``` sh
jrnl --format pretty
# or
jrnl -1 # any search
```

This is the default format in `jrnl`. If no `--format` is given, `pretty` will be used.

It displays the timestamp of each entry formatted to by the user config followed by the
title on the same line. Then the body of the entry is shown below.

This format is configurable through these values from your config file (see
[Advanced Usage](./advanced.md) for more details):

- `colors`
    - `body`
    - `date`
    - `tags`
    - `title`
- `indent_character`
- `linewrap`
- `timeformat`

**Example output**:
``` sh
2020-06-28 18:22 This is the first sample entry
| This is the sample body text of the first sample entry.

2020-07-01 20:00 This is the second sample entry
| This is the sample body text of the second sample entry, but
| this one has a @tag.

2020-07-02 09:00 This is the third sample entry
| This is the sample body text of the third sample entry.
```

### Short

``` sh
jrnl --format short
# or
jrnl --short
```

This will shorten entries to display only the date and title. It is essentially the
`pretty` format but without the body of each entry. This can be useful if you have long
journal entries and only want to see a list of entries that match your search.

**Example output**:
``` sh
2020-06-28 18:22 This is the first sample entry
2020-07-01 20:00 This is the second sample entry
2020-07-02 09:00 This is the third sample entry
```

### Fancy (or Boxed)
``` sh
jrnl --format fancy
# or
jrnl --format boxed
```

This format outlines each entry with a border. This makes it much easier to tell where
each entry starts and ends. It's an example of how free-form the formats can be, and also
just looks kinda ~*~fancy~*~, if you're into that kind of thing.

**Example output**:
``` sh
┎──────────────────────────────────────────────────────────────────────╮2020-06-28 18:22
┃ This is the first sample entry                                       ╘═══════════════╕
┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
┃ This is the sample body text of the first sample entry.                              │
┖──────────────────────────────────────────────────────────────────────────────────────┘
┎──────────────────────────────────────────────────────────────────────╮2020-07-01 20:00
┃ This is the second sample entry                                      ╘═══════════════╕
┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
┃ This is the sample body text of the second sample entry, but this one has a @tag.    │
┖──────────────────────────────────────────────────────────────────────────────────────┘
┎──────────────────────────────────────────────────────────────────────╮2020-07-02 09:00
┃ This is the third sample entry                                       ╘═══════════════╕
┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
┃ This is the sample body text of the third sample entry.                              │
┖──────────────────────────────────────────────────────────────────────────────────────┘
```

## Data Formats
These formats are mainly intended for piping or exporting your journal to other
programs. Even so, they can still be used in the same way as any other format (like
written to a file, or displayed in your terminal, if you want).

### JSON

``` sh
jrnl --format json
```

JSON is a very handy format used by many programs and has support in nearly every
programming language. There are many things you could do with JSON data. Maybe you could
use `jq` ([project page](https://github.com/stedolan/jq)) to filter through the fields in your journal.
Like this:

``` sh
$ j -3 --format json | jq '.entries[].date'                                                                                                                            jrnl-GFqVlfgP-py3.8 
"2020-06-28"
"2020-07-01"
"2020-07-02"
```

Or why not create a [beautiful timeline](http://timeline.knightlab.com/) of your journal?

**Example output**:
``` json
{
  "tags": {
    "@tag": 1
  },
  "entries": [
    {
      "title": "This is the first sample entry",
      "body": "This is the sample body text of the first sample entry.",
      "date": "2020-06-28",
      "time": "18:22",
      "tags": [],
      "starred": false
    },
    {
      "title": "This is the second sample entry",
      "body": "This is the sample body text of the second sample entry, but this one has a @tag.",
      "date": "2020-07-01",
      "time": "20:00",
      "tags": [
        "@tag"
      ],
      "starred": false
    },
    {
      "title": "This is the third sample entry",
      "body": "This is the sample body text of the third sample entry.",
      "date": "2020-07-02",
      "time": "09:00",
      "tags": [],
      "starred": false
    }
  ]
}
```

### Markdown

``` sh
jrnl --format markdown
# or
jrnl --format md
```

Markdown is a simple markup language that is human readable and can be used to be
rendered to other formats (html, pdf). `jrnl`'s
[README](https://github.com/jrnl-org/jrnl/blob/develop/README.md) for example is
formatted in markdown, then Github adds some formatting to make it look nice.

The markdown format groups entries by date (first by year, then by month), and adds
header markings as needed (e.g. `#`, `##`, etc). If you already have markdown header
markings in your journal, they will be incremented as necessary to make them fit under
these new headers (i.e. `#` will become `##`).

This format can be very useful, for example, to export a journal to a program that
converts markdown to html to make a website or a blog from your journal.

**Example output**:
``` markdown
# 2020

## June

### 2020-06-28 18:22 This is the first sample entry

This is the sample body text of the first sample entry.

## July

### 2020-07-01 20:00 This is the second sample entry

This is the sample body text of the second sample entry, but this one has a @tag.

### 2020-07-02 09:00 This is the third sample entry

This is the sample body text of the third sample entry.
```

### Plain Text

``` sh
jrnl --format text
# or
jrnl --format txt
```

This outputs your journal in the same plain-text format that `jrnl` uses to store your
journal on disk. This format is particularly useful for importing and exporting journals
within `jrnl`.

You can use it, for example, to move entries from one journal to another, or to create a
new journal with search results from another journal.

**Example output**:
``` sh
[2020-06-28 18:22] This is the first sample entry
This is the sample body text of the first sample entry.

[2020-07-01 20:00] This is the second sample entry
This is the sample body text of the second sample entry, but this one has a @tag.

[2020-07-02 09:00] This is the third sample entry
This is the sample body text of the third sample entry.
```

### XML
``` sh
jrnl --format xml
```

This outputs your journal into XML format. XML is a commonly used data format and is
supported by many programs and programming languages.

**Example output**:
``` xml
<?xml version="1.0" ?>
<journal>
        <entries>
                <entry date="2020-06-28T18:22:00" starred="">This is the first sample entry This is the sample body text of the first sample entry.</entry>
                <entry date="2020-07-01T20:00:00" starred="">
                        <tag name="@tag"/>
                        This is the second sample entry This is the sample body text of the second sample entry, but this one has a @tag.
                </entry>
                <entry date="2020-07-02T09:00:00" starred="">*This is the third sample entry, and is starred This is the sample body text of the third sample entry.</entry>
        </entries>
        <tags>
                <tag name="@tag">1</tag>
        </tags>
</journal>
```

### YAML
``` sh
jrnl --format yaml
```

This outputs your journal into YAML format. YAML is a commonly used data format and is
supported by many programs and programming languages.

**Example output**:
``` yaml
title: This is the second sample entry
date: 2020-07-01 20:00
starred: False
tags: tag

This is the sample body text of the second sample entry, but this one has a @tag.
```

## Report formats
Since formats use your journal data and display it in different ways, they can also be
used to create reports.

### Tags

``` sh
jrnl --format tags
# or
jrnl --tags
```

This format is a simple example of how formats can be used to create reports. It
displays each tag, and a count of how many entries in which tag appears in your journal
(or in the search results), sorted by most frequent.

Example output:
``` sh
@one                 : 32
@two                 : 17
@three               : 4
```

## Options

### Exporting with `--file`

Example: `jrnl --format json --file /some/path/to/a/file.txt`

By default, `jrnl` will output entries to your terminal. But if you provide `--file`
along with a filename, the same output that would have been to your terminal will be
written to the file instead. This is the same as piping the output to a file.

So, in bash for example, the following two statements are equivalent:

``` sh
jrnl --format json --file myjournal.json
```

``` sh
jrnl --format json > myjournal.json
```

#### Exporting to directories

If the `--file` argument is a directory, jrnl will export each entry into an individual file:

``` sh
jrnl --format json --file my_entries/
```

The contents of `my_entries/` will then look like this:

``` output
my_entries/
|- 2013_06_03_a-beautiful-day.json
|- 2013_06_07_dinner-with-gabriel.json
|- ...
```
