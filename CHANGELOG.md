Changelog
=========

### 1.0.2 (April 17, 2013)

* [Improved] Installs pycrypto by default
* [Improved] Removed clint in favour of colorama
* [Fixed] Smaller fixes and typos

### 1.0.1 (March 12, 2013)

* [Fixed] Requires parsedatetime 1.1.2 or newer

### 1.0.0 (March 4, 2013)

* [New] Integrates seamlessly with DayOne
* [Improved] Each journal can have individual settings
* [Fixed] A bug where jrnl would not go into compose mode
* [Fixed] A bug where jrnl would not add entries without timestamp
* [Fixed] Support for parsedatetime 1.x

### 0.3.2 (July 5, 2012)

* [Improved] Converts `\n` to new lines (if using directly on a command line, make sure to wrap your entry with quotes).

### 0.3.1 (June 16, 2012)

* [Improved] Supports deleting of last entry.
* [Fixed] Fixes a bug where --encrypt or --decrypt without a target file would not work.
* [Improved] Supports a config option for setting word wrap.
* [Improved] Supports multiple journal files.

### 0.3.0 (May 24, 2012)

* [Fixed] Dates such as "May 3" will now be interpreted as being in the past if the current day is at least 28 days in the future
* [Fixed] Bug where composed entry is lost when the journal file fails to load
* Changed directory structure and install scripts (removing the necessity to make an alias from `jrnl` to `jrnl.py`)

#### 0.2.4 (May 21, 2012)

* [Fixed] Parsing of new lines in journal files and entries
* [Improved] Adds support for encrypting and decrypting into new files

#### 0.2.3 (May 3, 2012)

* [Improved] Adds a `-short` option that will only display the titles of entries (or, when filtering by tags, the context of the tag)
* [Improved] Adds tag export
* [Improved] Adds coloured highlight of tags (by default, highlights all tags - when filtering by tags, only highlights search tags)
* [Improved] `.jrnl_config` will get automatically updated when updating jrnl to a new version

#### 0.2.2 (April 17, 2012)

* [Improved] Adds --encrypt and --decrypt to encrypt / decrypt existing journal files
* [Improved] Adds markdown export (kudos to dedan)

#### 0.2.1 (April 17, 2012)

* [Improved] Submitted to [PyPi](http://pypi.python.org/pypi/jrnl/0.2.1).

### 0.2.0 (April 16, 2012)

* [Improved] Encrypts using CBC
* [Fixed] `key` has been renamed to `password` in config to avoid confusion. (The key use to encrypt and decrypt a journal is the SHA256-hash of the password.)

#### 0.1.1 (April 15, 2012)

* [Fixed] Removed unnecessary print commands
* [Improved] Created the documentation

###  0.1.0 (April 13, 2012)

* [Improved] Supports encrypted journals using AES encryption
* [Improved] Support external editors for composing entries

#### 0.0.2 (April 5, 2012)

* [Improved] Filtering by tags and dates
* [Fixed] Now using dedicated classes for Journals and entries

#### 0.0.1 (March 29, 2012)

* Composing entries works. That's pretty much it.
