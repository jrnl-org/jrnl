# Overview

`jrnl` is a simple journal application for the command line.

`jrnl`'s goal is to facilitate the rapid creation and viewing of journal
entries. It is flexible enough to support different use cases and organization
strategies. It is powerful enough to search through thousands of entries and
display, or "filter," only the entries you want to see.

`jrnl` has most of the features you need, and few of the ones you don't.

## Plain Text

`jrnl` stores each journal in plain text. `jrnl` files can be stored anywhere,
including in shared folders to keep them synchronized between devices. Journal
files are compact (thousands of entries take up less than 1 MiB) and can be read
by almost any electronic device, now and for the foreseeable future.

## Tags

To make it easier to find entries later, `jrnl` includes support for inline tags
(the default tag symbol is `@`). Entries can be found and filtered 

## Support for Multiple Journals
  
`jrnl` includes support for the creation and management of multiple journals,
each of which can be stored as a single file or as a set of files. Entries are
automatically timestamped in a human-readable format that makes it easy to view
multiple entries at a time. `jrnl` can easily find the entries you want so that
you can read them or edit them.

## Support for External Editors

`jrnl` plays nicely with your favorite text editor. You may prefer to write
journal entries in an editor. Or you may want to make changes that require a
more comprehensive application. `jrnl` can filter specific entries and pass them
to the external editor of your choice.

## Encryption
  
`jrnl` includes support for [128-bit AES
encryption](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard) using
[cryptography.Fernet](https://cryptography.io/en/latest/fernet/). The
[encryption page](./encryption.md) explains `jrnl`'s cryptographic framework in
more detail.

## Import and Export

`jrnl` makes it easy to import entries from other sources. Existing entries can
be [exported](./export.md) in a variety of formats.

## Multi-Platform Support

`jrnl` is compatible with most operating systems. Pre-compiled binaries are
available through several distribution channels, and you can build from source.
See the [installation page](./installation.md) for more information.

## Open-Source

`jrnl` is written in [Python](https://www.python.org) and maintained by a
[friendly community](https://github.com/jrnl-org/jrnl) of open-source software
enthusiasts.
