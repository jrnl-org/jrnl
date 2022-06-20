<!--
Copyright (C) 2012-2022 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# Journal Types
`jrnl` can store your journal in a few different ways:

 - a single text file (encrypted or otherwise)
 - a folder structure organized by date containing unencrypted text files
 - the DayOne Classic format

There is no need to specify what type of journal you'd like to use. Instead,
`jrnl` will automatically detect the journal type based on whether you're
referencing a file or a folder in your [config file](advanced.md),
and if it's a folder, whether or not DayOne Classic content exists in it.

## Single File
The single file format is the most flexible, as it can be [encrypted](encryption.md).
To use it, enter any path that is a file or does not already exist. You can
use any extension. `jrnl` will automatically create the file when you save
your first entry.

## Folder
The folder journal format organizes your entries into subfolders for the year
and month and `.txt` files for each day. If there are multiple entries in a day,
they all appear in the same `.txt` file.

The directory tree structure is in this format: `YYYY/MM/DD.txt`. For instance, if
you have an entry on May 5th, 2021 in a folder journal at `~/folderjournal`, it will
be located in: `~/folderjournal/2021/05/05.txt`

!!! note
Creating a new folder journal can be done in two ways:

* Create a folder with the name of the journal before running `jrnl`. Otherwise, when you run `jrnl` for the first time, it will assume that you are creating a single file journal instead, and it will create a file at that path.
* Create a new journal in your [config_file](advanced.md) and end the path with a ``/`` (on a POSIX system like Linux or MacOSX) or a ``\`` (on a Windows system). The folder will be created automatically if it doesn't exist.

!!! note
Folder journals can't be encrypted.

## Day One Classic
`jrnl` supports the original data format used by DayOne. It's similar to the folder
journal format, except it's identified by either of these characteristics:

* the folder has a `.dayone` extension
* the folder has a subfolder named `entries`

This is not to be confused with the DayOne 2.0 format, [which is very different](https://help.dayoneapp.com/en/articles/1187337-day-one-classic-is-retired).

!!! note
DayOne Classic journals can't be encrypted.

## Changing your journal type
You can't simply modify a journal's configuration to change its type. Instead,
define a new journal as the type you'd like, and use
[piping](https://en.wikipedia.org/wiki/Redirection_(computing)#Piping)
to export your old journal as `txt` to an import command on your new journal.

For instance, if you have a `projects` journal you would like to import into
a `new` journal, you would run the following after setting up the configuration
for your `new` journal:
```
jrnl projects --format txt | jrnl new --import
```
