Changelog
=========

### 0.2.3

* Adds a `-short` option that will only display the titles of entries (or, when filtering by tags, the context of the tag)
* Adds tag export
* Adds coloured highlight of tags (by default, highlights all tags - when filtering by tags, only highlights search tags)
* `.jrnl_config` will get automatically updated when updating jrnl to a new version

### 0.2.2

* Adds --encrypt and --decrypt to encrypt / descrypt existing journal files
* Adds markdown export (kudos to dedan)

### 0.2.1

* Submitted to [PyPi](http://pypi.python.org/pypi/jrnl/0.2.1).

### 0.2.0

* Encrypts using CBC
* `key` has been renamed to `password` in config to avoid confusion. (The key use to encrypt and decrypt a journal is the SHA256-hash of the password.)

### 0.1.1

* Removed unnecessary print commands
* Created the documentation

###  0.1.0

* Supports encrypted journals using AES encryption
* Support external editors for composing entries

### 0.0.2

* Filtering by tags and dates
* Now using dedicated classes for Journals and entries

### 0.0.1

* Composing entries works. That's pretty much it.
