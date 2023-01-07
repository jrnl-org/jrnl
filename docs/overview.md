<!--
Copyright © 2012-2023 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# Overview

`jrnl` is a simple journal application for the command line.

You can use it to easily create, search, and view journal entries. Journals are
stored as human-readable plain text, and can also be encrypted using [AES
encryption](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard).

`jrnl` has most of the features you need, and few of the ones you don't.

## Plain Text

`jrnl` stores each journal in plain text. You can store `jrnl` files anywhere,
including in shared folders to keep them synchronized between devices. Journal
files are compact (thousands of entries take up less than 1 MiB) and can be read
by almost any electronic device, now and for the foreseeable future.

## Tags

To make it easier to find entries later, `jrnl` includes support for inline tags
(the default tag symbol is `@`). You can find and filter entries by using tags
along with other search criteria.

## Support for Multiple Journals
  
`jrnl` includes support for the creation of multiple journals, each of which
can be stored as a single file or as a set of files. Entries are automatically
timestamped in a human-readable format that makes it easy to view multiple
entries at a time. `jrnl` can easily find the entries you want so that you can
read them or edit them.

## Support for External Editors

`jrnl` plays nicely with your favorite text editor. You may prefer to write
journal entries in an editor. Or you may want to make changes that require a
more comprehensive application. `jrnl` can filter specific entries and pass them
to the [external editor](./external-editors.md) of your choice.

## Encryption
  
`jrnl` includes support for [AES
encryption](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard). See the
[encryption page](./encryption.md) for more information.

## Import and Export

`jrnl` makes it easy to import entries from other sources. Existing entries can
be exported in a variety of [formats](./formats.md).

## Multi-Platform Support

`jrnl` is compatible with most operating systems. You can [download](./installation.md) it using one
of a variety of package managers, or you can build from source.

## Open-Source

`jrnl` is written in [Python](https://www.python.org) and maintained by a
[friendly community](https://github.com/jrnl-org/jrnl) of open-source software
enthusiasts.
