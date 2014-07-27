Changelog
=========


### 1.9 (July 21, 2014)

* __1.9.2__ Fixed: Tag search ignores email-addresses (thanks to @mjhoffman65)
* __1.9.1__ Fixed: Dates in the future can be parsed as well.
* __1.9.0__ Improved: Greatly improved date parsing. Also added an `-on` option for filtering

### 1.8 (May 22, 2014)

* __1.8.7__ Fixed: -from and -to filters are inclusive (thanks to @grplyler)
* __1.8.6__ Improved: Tags like @C++ and @OS/2 work, too (thanks to @chaitan94)
* __1.8.5__ Fixed: file names when exporting to individual files contain full year (thanks to @jdevera)
* __1.8.4__ Improved: using external editors (thanks to @chrissexton)
* __1.8.3__ Fixed: export to text files and improves help (thanks to @igniteflow and @mpe)
* __1.8.2__ Better integration with environment variables (thanks to @ajaam and @matze)
* __1.8.1__ Minor bug fixes
* __1.8.0__ Official support for python 3.4

### 1.7 (December 22, 2013)

* __1.7.22__ Fixed an issue with writing files when exporting entries containing non-ascii characters.
* __1.7.21__ jrnl now uses PKCS#7 padding.
* __1.7.20__ Minor fixes when parsing DayOne journals
* __1.7.19__ Creates full path to journal during installation if it doesn't exist yet
* __1.7.18__ Small update to parsing regex
* __1.7.17__ Fixes writing new lines between entries
* __1.7.16__ Even more unicode fixes!
* __1.7.15__ More unicode fixes
* __1.7.14__ Fix for trailing whitespaces (eg. when writing markdown code block)
* __1.7.13__ Fix for UTF-8 in DayOne journals
* __1.7.12__ Fixes a bug where filtering by tags didn't work for DayOne journals
* __1.7.11__ `-ls` will list all available journals (Thanks @jtan189)
* __1.7.10__ Supports `-3` as a shortcut for `-n 3` and updates to tzlocal 1.1
* __1.7.9__ Fix a logic bug so that jrnl -h and jrnl -v are possible even if jrnl not configured yet.
* __1.7.8__ Upgrade to parsedatetime 1.2
* __1.7.7__ Cleaned up imports, better unicode support
* __1.7.6__ Python 3 port for slugify
* __1.7.5__ Colorama is only needed on Windows. Smaller fixes
* __1.7.3__ Touches temporary files before opening them to allow more external editors.
* __1.7.2__ Dateutil added to requirements.
* __1.7.1__ Fixes issues with parsing time information in entries.
* __1.7.0__ Edit encrypted or DayOne journals with `jrnl --edit`.


### 1.6 (November 5, 2013)

* __1.6.6__ -v prints the current version, also better strings for windows users. Furthermore, jrnl/jrnl.py moved to jrnl/cli.py
* __1.6.5__ Allows composing multi-line entries on the command line or importing files
* __1.6.4__ Fixed a bug that caused creating encrypted journals to fail
* __1.6.3__ New, pretty, _useful_ documentation!
* __1.6.2__ Starring entries now works for plain-text journals too!
* __1.6.1__ Attempts to fix broken config files automatically
* __1.6.0__ Passwords are now saved in the key-chain. The `password` field in `.jrnl_config` is soft-deprecated.

### 1.5 (August 6, 2013)

* __1.5.7__ The `~` in journal config paths will now expand properly to e.g. `/Users/maebert`
* __1.5.6__ Fixed: Fixed a bug where on OS X, the timezone could only be accessed on administrator accounts.
* __1.5.5__ Fixed: Detects DayOne journals stored in `~/Library/Mobile Data` as well.
* __1.5.4__ DayOne journals can now handle tags
* __1.5.3__ Fixed: DayOne integration with older DayOne Journals
* __1.5.2__ Soft-deprecated `-to` for filtering by time and introduces `-until` instead.
* __1.5.1__ Fixed: Fixed a bug introduced in 1.5.0 that caused the entire journal to be printed after composing an entry
* __1.5.0__ Exporting, encrypting and displaying tags now takes your filter options into account. So you could export everything before May 2012: `jrnl -to 'may 2012' --export json`. Or encrypt all entries tagged with `@work` into a new journal: `jrnl @work --encrypt work_journal.txt`. Or display all tags of posts where Bob is also tagged: `jrnl @bob --tags`

### 1.4 (July 22, 2013)

* __1.4.2__ Fixed: Tagging works again
* __1.4.0__ Unifies encryption between Python 2 and 3. If you have problems reading encrypted journals afterwards, first decrypt your journal with the __old__ jrnl version (install with `pip install jrnl==1.3.1`, then `jrnl --decrypt`), upgrade jrnl (`pip install jrnl --upgrade`) and encrypt it again (`jrnl --encrypt`).

### 1.3 (July 17, 2013)

* __1.3.2__ Everything that is not direct output of jrnl will be written stderr to improve integration
* __1.3.0__ Export to multiple files
* __1.3.0__ Feature to export to given output file

### 1.2 (July 15, 2013)

* __1.2.0__ Fixed: Timezone support for DayOne


### 1.1 (June 9, 2013)

* __1.1.1__ Fixed: Unicode and Python3 issues resolved.
* __1.1.0__
    * JSON export exports tags as well.
    * Nicer error message when there is a syntactical error in your config file.
    * Unicode support

### 1.0 (March 4, 2013)

* __1.0.5__ Backwards compatibility with `parsedatetime` 0.8.7
* __1.0.4__
    * Python 2.6 compatibility
    * Better utf-8 support
    * Python 3 compatibility
    * Respects the `XDG_CONFIG_HOME` environment variable for storing your configuration file (Thanks [evaryont](https://github.com/evaryont))

* __1.0.3__
    * Removed clint in favour of colorama
    * Fixed: Fixed a bug where showing tags failed when no tags are defined.
    * Fixed: Improvements to config parsing (Thanks [alapolloni](https://github.com/alapolloni))
    * Fixed: Fixes readline support on Windows
    * Fixed: Smaller fixes and typos
* __1.0.1__ (March 12, 2013) Fixed: Requires parsedatetime 1.1.2 or newer
* __1.0.0__
    * Integrates seamlessly with DayOne
    * Each journal can have individual settings
    * Fixed: A bug where jrnl would not go into compose mode
    * Fixed: A bug where jrnl would not add entries without timestamp
    * Fixed: Support for parsedatetime 1.x

### 0.3 (May 24, 2012)

* __0.3.2__ Converts `\n` to new lines (if using directly on a command line, make sure to wrap your entry with quotes).
* __0.3.1__
    * Supports deleting of last entry.
    * Fixed: Fixes a bug where --encrypt or --decrypt without a target file would not work.
    * Supports a config option for setting word wrap.
    * Supports multiple journal files.
* __0.3.0__
    * Fixed: Dates such as "May 3" will now be interpreted as being in the past if the current day is at least 28 days in the future
    * Fixed: Bug where composed entry is lost when the journal file fails to load
    * Changed directory structure and install scripts (removing the necessity to make an alias from `jrnl` to `jrnl.py`)

### 0.2 (April 16, 2012)

* __0.2.4__
    * Fixed: Parsing of new lines in journal files and entries
    * Adds support for encrypting and decrypting into new files
* __0.2.3__
    * Adds a `-short` option that will only display the titles of entries (or, when filtering by tags, the context of the tag)
    * Adds tag export
    * Adds coloured highlight of tags (by default, highlights all tags - when filtering by tags, only highlights search tags)
    * `.jrnl_config` will get automatically updated when updating jrnl to a new version
* __0.2.2__
    * Adds --encrypt and --decrypt to encrypt / decrypt existing journal files
    * Adds markdown export (kudos to dedan)
* __0.2.1__ Submitted to [PyPi](http://pypi.python.org/pypi/jrnl/0.2.1).
* __0.2.0__
    * Encrypts using CBC
    * Fixed: `key` has been renamed to `password` in config to avoid confusion. (The key use to encrypt and decrypt a journal is the SHA256-hash of the password.)

### 0.1 (April 13, 2012)


* __0.1.1__
    * Fixed: Removed unnecessary print commands
    * Created the documentation
* __0.1.0__
    * Supports encrypted journals using AES encryption
    * Support external editors for composing entries
* __0.0.2__
    * Filtering by tags and dates
    * Fixed: Now using dedicated classes for Journals and entries

### 0.0 (March 29, 2012)

* __0.0.1__ Composing entries works. That's pretty much it.
