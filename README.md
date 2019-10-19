jrnl [![Build Status](https://travis-ci.com/jrnl-org/jrnl.svg?branch=master)](https://travis-ci.com/jrnl-org/jrnl) [![Downloads](https://pepy.tech/badge/jrnl)](https://pepy.tech/project/jrnl) [![Version](http://img.shields.io/pypi/v/jrnl.svg?style=flat)](https://pypi.python.org/pypi/jrnl/)
====

_To get help, [submit an issue](https://github.com/jrnl-org/jrnl/issues/new) on Github._

*jrnl* is a simple journal application for your command line. Journals are stored as human readable plain text files - you can put them into a Dropbox folder for instant syncing and you can be assured that your journal will still be readable in 2050, when all your fancy iPad journal applications will long be forgotten.

Optionally, your journal can be encrypted using the [256-bit AES](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard).

### Why keep a journal?

Journals aren't just for people who have too much time on their summer vacation. A journal helps you to keep track of the things you get done and how you did them. Your imagination may be limitless, but your memory isn't. For personal use, make it a good habit to write at least 20 words a day. Just to reflect what made this day special, why you haven't wasted it. For professional use, consider a text-based journal to be the perfect complement to your GTD todo list - a documentation of what and how you've done it.

In a Nutshell
-------------

to make a new entry, just type

    jrnl yesterday: Called in sick. Used the time to clean the house and spent 4h on writing my book.

and hit return. `yesterday:` will be interpreted as a timestamp. Everything until the first sentence mark (`.?!`) will be interpreted as the title, the rest as the body. In your journal file, the result will look like this:

    2012-03-29 09:00 Called in sick.
    Used the time to clean the house and spent 4h on writing my book.

If you just call `jrnl`, you will be prompted to compose your entry - but you can also configure _jrnl_ to use your external editor.

Known Issues
------------
jrnl used to support integration with Day One, but no longer supports it since Day One 2 was released with a different backend. [See the GitHub issue for more information](https://github.com/jrnl-org/jrnl/issues/409).

Authors
-------
Current maintainers:

 * Jonathan Wren ([wren](https://github.com/wren))
 * Micah Ellison ([micahellison](https://github.com/micahellison))

Original maintainer:

 * Manuel Ebert ([maebert](https://github.com/maebert))
