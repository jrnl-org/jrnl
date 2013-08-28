Changelog
=========

#### 1.5.5

* [Fixed] Detects DayOne journals stored in `~/Library/Mobile Data` as well.

#### 1.5.4

* [New] DayOne journals can now handle tags

#### 1.5.3

* [Fixed] DayOne integration with older DayOne Journals

#### 1.5.2

* [Improved] Soft-deprecated `-to` for filtering by time and introduces `-until` instead.

#### 1.5.1

* [Fixed] Fixed a bug introduced in 1.5.0 that caused the entire journal to be printed after composing an entry

### 1.5.0

* [Improved] Exporting, encrypting and displaying tags now takes your filter options into account. So you could export everything before May 2012: `jrnl -to 'may 2012' --export json`. Or encrypt all entries tagged with `@work` into a new journal: `jrnl @work --encrypt work_journal.txt`. Or display all tags of posts where Bob is also tagged: `jrnl @bob --tags`

#### 1.4.2

* [Fixed] Tagging works again
* Meta-info for PyPi updated

### 1.4.0

* [Improved] Unifies encryption between Python 2 and 3. If you have problems reading encrypted journals afterwards, first decrypt your journal with the __old__ jrnl version (install with `pip install jrnl==1.3.1`, then `jrnl --decrypt`), upgrade jrnl (`pip install jrnl --upgrade`) and encrypt it again (`jrnl --encrypt`).

#### 1.3.2

* [Improved] Everything that is not direct output of jrnl will be written stderr to improve integration

### 1.3.0

* [New] Export to multiple files
* [New] Feature to export to given output file

#### 1.1.2

* [Fixed] Timezone support for DayOne

#### 1.1.1

* [Fixed] Unicode and Python3 issues resolved.

### 1.1.0

* [New] JSON export exports tags as well.
* [Improved] Nicer error message when there is a syntactical error in your config file.
* [Improved] Unicode support

#### 1.0.5

* [Improved] Backwards compatibility with `parsedatetime` 0.8.7

#### 1.0.4

* [Improved] Python 2.6 compatibility
* [Improved] Better utf-8 support
* [New] Python 3 compatibility
* [New] Respects the `XDG_CONFIG_HOME` environment variable for storing your configuration file (Thanks [evaryont](https://github.com/evaryont))

#### 1.0.3 (April 17, 2013)

* [Improved] Removed clint in favour of colorama
* [Fixed] Fixed a bug where showing tags failed when no tags are defined.
* [Fixed] Improvements to config parsing (Thanks [alapolloni](https://github.com/alapolloni))
* [Fixed] Fixes readline support on Windows
* [Fixed] Smaller fixes and typos

#### 1.0.1 (March 12, 2013)

* [Fixed] Requires parsedatetime 1.1.2 or newer

### 1.0.0 (March 4, 2013)

* [New] Integrates seamlessly with DayOne
* [Improved] Each journal can have individual settings
* [Fixed] A bug where jrnl would not go into compose mode
* [Fixed] A bug where jrnl would not add entries without timestamp
* [Fixed] Support for parsedatetime 1.x

#### 0.3.2 (July 5, 2012)

* [Improved] Converts `\n` to new lines (if using directly on a command line, make sure to wrap your entry with quotes).

#### 0.3.1 (June 16, 2012)

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
