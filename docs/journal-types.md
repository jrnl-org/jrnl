<!-- Copyright (C) 2012-2021 jrnl contributors
     License: https://www.gnu.org/licenses/gpl-3.0.html -->
# Journal Types
`jrnl` can store your journal in a few different ways:

 - a single text file (encrypted or otherwise)
 - a folder structure organized by date containing unencrypted text files
 - the DayOne Classic format, which is a folder structure containing 

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
When creating a new folder journal, you will need to create the folder before running
`jrnl`. Otherwise, when you run `jrnl` for the first time, it will assume that you
are creating a single file journal instead, and it will create a file at that path.

!!! note
Folder journals can't be encrypted.

## Day One Classic
`jrnl` supports the original data format used by DayOne. It's very similar to the folder
journal format, except it's identified by either of these characteristics:

* the folder has a `.dayone` extension
* the folder has a subfolder named `entries`

This is not to be confused with the DayOne 2.0 format, which is very different.

!!! note
DayOne Classic journals can't be encrypted.
