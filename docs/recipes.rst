.. _recipes:

FAQ
===

Recipes
-------


~~~~~~~~~~~~~~~~


Known Issues
------------

- The Windows shell prior to Windows 7 has issues with unicode encoding. If you want to use non-ascii characters, change the codepage with ``chcp 1252`` before using `jrnl` (Thanks to Yves Pouplard for solving this!)
- _jrnl_ relies on the `PyCrypto` package to encrypt journals, which has some known problems with installing on Windows and within virtual environments.
