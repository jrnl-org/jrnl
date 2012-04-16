Changelog
=========

### 0.2.0

* Encrypts using CBC
* `key` has been renamed to `password` in config to avoid confusion. (The key use to encrypt and decrypt a journal is the SHA256-hash of the password.)

### 0.1.1

* Removed unnecessary print commands
* Created the documentation
* Registered jrnl in the python package repository

###  0.1.0

* Supports encrypted journals using AES encryption
* Support external editors for composing entries

### 0.0.2

* Filtering by tags and dates
* Now using dedicated classes for Journals and entries

### 0.0.1

* Composing entries works. That's pretty much it.
