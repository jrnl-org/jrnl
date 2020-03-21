# Changelog

## [Unreleased](https://github.com/jrnl-org/jrnl/)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.2...HEAD)

**Implemented enhancements:**

- Update YAML exporter to handle Dayone format [\#773](https://github.com/jrnl-org/jrnl/pull/773) ([MinchinWeb](https://github.com/MinchinWeb))

**Fixed bugs:**

- Listing all entries in DayOne Classic journal throws IndexError [\#786](https://github.com/jrnl-org/jrnl/pull/786) ([MinchinWeb](https://github.com/MinchinWeb))
- Add UTC support for failing DayOne tests [\#785](https://github.com/jrnl-org/jrnl/pull/785) ([MinchinWeb](https://github.com/MinchinWeb))

**Build:**

- Stop multiple changelog generators from crashing into each other [\#845](https://github.com/jrnl-org/jrnl/pull/845) ([wren](https://github.com/wren))
- Don't re-run tests on deployment [\#839](https://github.com/jrnl-org/jrnl/pull/839) ([wren](https://github.com/wren))
- Put back build lines in Poetry config [\#838](https://github.com/jrnl-org/jrnl/pull/838) ([wren](https://github.com/wren))
- Restore emoji test [\#837](https://github.com/jrnl-org/jrnl/pull/837) ([micahellison](https://github.com/micahellison))
- Fix crashing unicode Travis tests on Windows and fail build if Windows tests fail [\#836](https://github.com/jrnl-org/jrnl/pull/836) ([micahellison](https://github.com/micahellison))
- Remove poetry from build system in pyproject config to fix `brew install` [\#830](https://github.com/jrnl-org/jrnl/pull/830) ([wren](https://github.com/wren))
- Fix all skipped tests on Travis Windows builds by preserving newlines [\#823](https://github.com/jrnl-org/jrnl/pull/823) ([micahellison](https://github.com/micahellison))

**Updated documentation:**

- Docs: Fix broken links in recipes.md [\#854](https://github.com/jrnl-org/jrnl/pull/854) ([lrvl](https://github.com/lrvl))
- Fix fish history instructions. [\#846](https://github.com/jrnl-org/jrnl/pull/846) ([aureooms](https://github.com/aureooms))
- Update site description [\#841](https://github.com/jrnl-org/jrnl/pull/841) ([wren](https://github.com/wren))
- Get rid of dumb sex joke [\#840](https://github.com/jrnl-org/jrnl/pull/840) ([wren](https://github.com/wren))
- Updating/clarifying template explanation [\#829](https://github.com/jrnl-org/jrnl/pull/829) ([heymajor](https://github.com/heymajor))

## [v2.2](https://pypi.org/project/jrnl/v2.2/) (2020-02-01)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.1.1...v2.2)


**Implemented enhancements:**

- Update YAML exporter to handle Dayone format [\#773](https://github.com/jrnl-org/jrnl/pull/773) ([MinchinWeb](https://github.com/MinchinWeb))
- Full text search \(case insensitive\) with "-contains" [\#740](https://github.com/jrnl-org/jrnl/pull/740) ([empireshades](https://github.com/empireshades))
- Reduce startup time by 55% [\#719](https://github.com/jrnl-org/jrnl/pull/719) ([maebert](https://github.com/maebert))
- Refactor password logic to prevent accidental password leakage [\#708](https://github.com/jrnl-org/jrnl/pull/708) ([pspeter](https://github.com/pspeter))
- Password confirmation [\#706](https://github.com/jrnl-org/jrnl/pull/706) ([pspeter](https://github.com/pspeter))

**Fixed bugs:**

- Close temp file before passing it to editor to prevent file locking issues in Windows [\#792](https://github.com/jrnl-org/jrnl/pull/792) ([micahellison](https://github.com/micahellison))
- Fix crash while encrypting a journal on first run without saving password [\#789](https://github.com/jrnl-org/jrnl/pull/789) ([dbxnr](https://github.com/dbxnr))

**Build:**

- Fix issue where jrnl would always out 'source' for version, fix Poetry config to build and publish properly [\#820](https://github.com/jrnl-org/jrnl/pull/820) ([wren](https://github.com/wren))
- Unpin poetry [\#808](https://github.com/jrnl-org/jrnl/pull/808) ([wren](https://github.com/wren))
- Fix all skipped tests on Travis Windows builds by preserving newlines [\#823](https://github.com/jrnl-org/jrnl/pull/823) ([micahellison](https://github.com/micahellison))
- Change PyPI auth method in build pipeline [\#807](https://github.com/jrnl-org/jrnl/pull/807) ([wren](https://github.com/wren))
- Automagically update the changelog you see before your very eyes! [\#806](https://github.com/jrnl-org/jrnl/pull/806) ([wren](https://github.com/wren))
- Update Black version and lock file to fix builds on develop branch [\#784](https://github.com/jrnl-org/jrnl/pull/784) ([wren](https://github.com/wren))
- Run black formatter on codebase for standardization [\#778](https://github.com/jrnl-org/jrnl/pull/778) ([wren](https://github.com/wren))
- Skip Broken Windows Tests [\#772](https://github.com/jrnl-org/jrnl/pull/772) ([wren](https://github.com/wren))
- Black Formatter [\#769](https://github.com/jrnl-org/jrnl/pull/769) ([MinchinWeb](https://github.com/MinchinWeb))
- Update lock file and testing suite for Python 3.8 [\#765](https://github.com/jrnl-org/jrnl/pull/765) ([wren](https://github.com/wren))
- Fix CI config to only deploy once [\#761](https://github.com/jrnl-org/jrnl/pull/761) ([wren](https://github.com/wren))
- More Travis-CI Testing [\#759](https://github.com/jrnl-org/jrnl/pull/759) ([MinchinWeb](https://github.com/MinchinWeb))

**Updated documentation:**

- Explain how fish can be configured to exclude jrnl commands from history by default [\#809](https://github.com/jrnl-org/jrnl/pull/809) ([aureooms](https://github.com/aureooms))
- Remove merge marker in recipes.md [\#782](https://github.com/jrnl-org/jrnl/pull/782) ([markphelps](https://github.com/markphelps))
- Fix merge conflict left-over [\#767](https://github.com/jrnl-org/jrnl/pull/767) ([thejspr](https://github.com/thejspr))
- Display header in docs on mobile devices [\#763](https://github.com/jrnl-org/jrnl/pull/763) ([maebert](https://github.com/maebert))

## [v2.1.1](https://pypi.org/project/jrnl/v2.1.1/) (2019-11-26)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.1.post2...v2.1.1)

**Implemented enhancements:**

- Support Python 3.6+ [\#710](https://github.com/jrnl-org/jrnl/pull/710) ([pspeter](https://github.com/pspeter))
- Drop Python 2 support, add mocks in tests [\#705](https://github.com/jrnl-org/jrnl/pull/705) ([pspeter](https://github.com/pspeter))

**Fixed bugs:**

- Prevent readline usage on Windows, which was causing Active Python crashes on install [\#751](https://github.com/jrnl-org/jrnl/pull/751) ([micahellison](https://github.com/micahellison))
- Exit jrnl if no text entered into editor [\#744](https://github.com/jrnl-org/jrnl/pull/744) ([alichtman](https://github.com/alichtman))
- Fix crash when no keyring backend available [\#699](https://github.com/jrnl-org/jrnl/pull/699) ([pspeter](https://github.com/pspeter))
- Fix parsing Journals using a little-endian date format [\#694](https://github.com/jrnl-org/jrnl/pull/694) ([pspeter](https://github.com/pspeter))

**Updated documentation:**

- Update developer documentation [\#752](https://github.com/jrnl-org/jrnl/pull/752) ([micahellison](https://github.com/micahellison))
- Create templates for issues and pull requests [\#679](https://github.com/jrnl-org/jrnl/pull/679) ([C0DK](https://github.com/C0DK))
- Smaller doc fixes [\#649](https://github.com/jrnl-org/jrnl/pull/649) ([maebert](https://github.com/maebert))
- Move to mkdocs [\#611](https://github.com/jrnl-org/jrnl/pull/611) ([maebert](https://github.com/maebert))

## [v2.1.post2](https://pypi.org/project/jrnl/v2.1.post2/) (2019-11-11)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.0.1...v2.1.post2)

**Fixed bugs:**

- Expand paths that use ~ to full path [\#704](https://github.com/jrnl-org/jrnl/pull/704) ([MinchinWeb](https://github.com/MinchinWeb))

**Build:**

- Separate local dev from pipeline releases [\#684](https://github.com/jrnl-org/jrnl/pull/684) ([wren](https://github.com/wren))
- Update version handling in source and travis deployments [\#683](https://github.com/jrnl-org/jrnl/pull/683) ([wren](https://github.com/wren))
- Use Poetry for dependency management and deployments [\#612](https://github.com/jrnl-org/jrnl/pull/612) ([maebert](https://github.com/maebert))

**Updated documentation:**

- Fix typos, spelling [\#734](https://github.com/jrnl-org/jrnl/pull/734) ([MinchinWeb](https://github.com/MinchinWeb))

## [v2.0.1](https://pypi.org/project/jrnl/v2.0.1/) (2019-09-26)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/v2.0.0...v2.0.1)

**Implemented enhancements:**

- Switch to hashmark Markdown headers on export \(Mk II\) [\#639](https://github.com/jrnl-org/jrnl/pull/639) ([MinchinWeb](https://github.com/MinchinWeb))
- Add '-not' flag for excluding tags from filter [\#637](https://github.com/jrnl-org/jrnl/pull/637) ([jprof](https://github.com/jprof))
- Handle KeyboardInterrupt when installing journal [\#550](https://github.com/jrnl-org/jrnl/pull/550) ([silenc3r](https://github.com/silenc3r))

**Fixed bugs:**

- Change pyYAML required version [\#660](https://github.com/jrnl-org/jrnl/pull/660) ([etnnth](https://github.com/etnnth))

**Updated documentation:**

- Fix references to Sphinx in CONTRIBUTING.md [\#655](https://github.com/jrnl-org/jrnl/pull/655) ([maebert](https://github.com/maebert))

## [v2.0.0](https://pypi.org/project/jrnl/v2.0.0/) (2019-08-24)

[Full Changelog](https://github.com/jrnl-org/jrnl/compare/1.9.8...v2.0.0)

🚨 **BREAKING CHANGES** 🚨

**Implemented enhancements:**
- Change cryptographic backend from PyCrypto to cryptography.io
- Config now respects XDG conventions and may move accordingly
- Config name changed from `journals.jrnl_name.journal` to `journals.jrnl_name.path`

**Fixed bugs:**

- Confirm that each journal can be parsed during upgrade, and abort upgrade if not [\#650](https://github.com/jrnl-org/jrnl/pull/650) ([micahellison](https://github.com/micahellison))
- Escape dates in square brackets [\#644](https://github.com/jrnl-org/jrnl/pull/644) ([wren](https://github.com/wren))
- Create encrypted journal [\#641](https://github.com/jrnl-org/jrnl/pull/641) ([gregorybodnar](https://github.com/gregorybodnar))
- Resolve issues around unreadable dates to allow markdown footnotes and prevent accidental deletion [\#623](https://github.com/jrnl-org/jrnl/pull/623) ([micahellison](https://github.com/micahellison))
- Update crypto module \#610 [\#621](https://github.com/jrnl-org/jrnl/pull/621) ([wren](https://github.com/wren))
- Fix issue \#584 YAMLLoadWarning [\#585](https://github.com/jrnl-org/jrnl/pull/585) ([wren](https://github.com/wren))

**Deprecated:**

- Deprecate Python 2 [\#624](https://github.com/jrnl-org/jrnl/pull/624) ([micahellison](https://github.com/micahellison))
- Config now saved as YAML (no more JSON)

**Build:**

- change pinned label to a super cool emoji ⭐️ [\#646](https://github.com/jrnl-org/jrnl/pull/646) ([wren](https://github.com/wren))
- Update Travis build badge and restore pypi badges [\#603](https://github.com/jrnl-org/jrnl/pull/603) ([micahellison](https://github.com/micahellison))

**Updated documentation:**

- Mention lack of Day One support and relevant history in readme [\#608](https://github.com/jrnl-org/jrnl/pull/608) ([micahellison](https://github.com/micahellison))
- Add a code of conduct file \(rather than adding to contributing\) [\#604](https://github.com/jrnl-org/jrnl/pull/604) ([wren](https://github.com/wren))
- Update docs to reflect merging jrnl-plus fork back upstream [\#601](https://github.com/jrnl-org/jrnl/pull/601) ([micahellison](https://github.com/micahellison))
- Add instructions for VS Code [\#544](https://github.com/jrnl-org/jrnl/pull/544) ([emceeaich](https://github.com/emceeaich))

## v1.9 (2014-07-21)

* __1.9.5__ Multi-word tags for DayOne Journals
* __1.9.4__ Fixed: Order of journal entries in file correct after --edit'ing
* __1.9.3__ Fixed: Tags at the beginning of lines
* __1.9.2__ Fixed: Tag search ignores email-addresses (thanks to @mjhoffman65)
* __1.9.1__ Fixed: Dates in the future can be parsed as well.
* __1.9.0__ Improved: Greatly improved date parsing. Also added an `-on` option for filtering

## v1.8 (2014-05-22)

* __1.8.7__ Fixed: -from and -to filters are inclusive (thanks to @grplyler)
* __1.8.6__ Improved: Tags like @C++ and @OS/2 work, too (thanks to @chaitan94)
* __1.8.5__ Fixed: file names when exporting to individual files contain full year (thanks to @jdevera)
* __1.8.4__ Improved: using external editors (thanks to @chrissexton)
* __1.8.3__ Fixed: export to text files and improves help (thanks to @igniteflow and @mpe)
* __1.8.2__ Better integration with environment variables (thanks to @ajaam and @matze)
* __1.8.1__ Minor bug fixes
* __1.8.0__ Official support for python 3.4

## v1.7 (2013-12-22)

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


## v1.6 (2013-11-05)

* __1.6.6__ -v prints the current version, also better strings for windows users. Furthermore, jrnl/jrnl.py moved to jrnl/cli.py
* __1.6.5__ Allows composing multi-line entries on the command line or importing files
* __1.6.4__ Fixed a bug that caused creating encrypted journals to fail
* __1.6.3__ New, pretty, _useful_ documentation!
* __1.6.2__ Starring entries now works for plain-text journals too!
* __1.6.1__ Attempts to fix broken config files automatically
* __1.6.0__ Passwords are now saved in the key-chain. The `password` field in `.jrnl_config` is soft-deprecated.

## v1.5 (2013-08-06)

* __1.5.7__ The `~` in journal config paths will now expand properly to e.g. `/Users/maebert`
* __1.5.6__ Fixed: Fixed a bug where on OS X, the timezone could only be accessed on administrator accounts.
* __1.5.5__ Fixed: Detects DayOne journals stored in `~/Library/Mobile Data` as well.
* __1.5.4__ DayOne journals can now handle tags
* __1.5.3__ Fixed: DayOne integration with older DayOne Journals
* __1.5.2__ Soft-deprecated `-to` for filtering by time and introduces `-until` instead.
* __1.5.1__ Fixed: Fixed a bug introduced in 1.5.0 that caused the entire journal to be printed after composing an entry
* __1.5.0__ Exporting, encrypting and displaying tags now takes your filter options into account. So you could export everything before May 2012: `jrnl -to 'may 2012' --export json`. Or encrypt all entries tagged with `@work` into a new journal: `jrnl @work --encrypt work_journal.txt`. Or display all tags of posts where Bob is also tagged: `jrnl @bob --tags`

## v1.4 (2013-07-22)

* __1.4.2__ Fixed: Tagging works again
* __1.4.0__ Unifies encryption between Python 2 and 3. If you have problems reading encrypted journals afterwards, first decrypt your journal with the __old__ jrnl version (install with `pip install jrnl==1.3.1`, then `jrnl --decrypt`), upgrade jrnl (`pip install jrnl --upgrade`) and encrypt it again (`jrnl --encrypt`).

## v1.3 (2013-07-17)

* __1.3.2__ Everything that is not direct output of jrnl will be written stderr to improve integration
* __1.3.0__ Export to multiple files
* __1.3.0__ Feature to export to given output file

## v1.2 (2013-07-15)

* __1.2.0__ Fixed: Timezone support for DayOne


## v1.1 (2013-06-09)

* __1.1.1__ Fixed: Unicode and Python3 issues resolved.
* __1.1.0__
    * JSON export exports tags as well.
    * Nicer error message when there is a syntactical error in your config file.
    * Unicode support

## v1.0 (2013-03-04)

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

## v0.3 (2012-05-24)

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

## v0.2 (2012-04-16)

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

## v0.1 (2012-04-13)


* __0.1.1__
    * Fixed: Removed unnecessary print commands
    * Created the documentation
* __0.1.0__
    * Supports encrypted journals using AES encryption
    * Support external editors for composing entries
* __0.0.2__
    * Filtering by tags and dates
    * Fixed: Now using dedicated classes for Journals and entries

## v0.0 (2012-03-29)

* __0.0.1__ Composing entries works. That's pretty much it.


\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
