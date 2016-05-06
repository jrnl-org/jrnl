jrnl [![Build Status](http://img.shields.io/travis/maebert/jrnl.svg?style=flat)](https://travis-ci.org/maebert/jrnl)  [![Downloads](http://img.shields.io/pypi/dm/jrnl.svg?style=flat)](https://pypi.python.org/pypi/jrnl/) [![Version](http://img.shields.io/pypi/v/jrnl.svg?style=flat)](https://pypi.python.org/pypi/jrnl/)
====

_For news on updates or to get help, [read the docs](http://maebert.github.io/jrnl/overview.html), follow [@maebert](https://twitter.com/maebert) or [submit an issue](https://github.com/maebert/jrnl/issues/new) on Github._

*jrnl* is a simple journal application for your command line. Journals are stored as human readable plain text files - you can put them into a Dropbox folder for instant syncing and you can be assured that your journal will still be readable in 2050, when all your fancy iPad journal applications will long be forgotten.

*jrnl* also plays nice with the fabulous [DayOne](http://dayoneapp.com/) and can read and write directly from and to DayOne Journals.

Optionally, your journal can be encrypted using the [256-bit AES](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard).

### Why keep a journal?

Journals aren't only for 13-year old girls and people who have too much time on their summer vacation. A journal helps you to keep track of the things you get done and how you did them. Your imagination may be limitless, but your memory isn't. For personal use, make it a good habit to write at least 20 words a day. Just to reflect what made this day special, why you haven't wasted it. For professional use, consider a text-based journal to be the perfect complement to your GTD todo list - a documentation of what and how you've done it.

In a Nutshell
-------------

to make a new entry, just type

    jrnl yesterday: Called in sick. Used the time to clean the house and spent 4h on writing my book.

and hit return. `yesterday:` will be interpreted as a timestamp. Everything until the first sentence mark (`.?!`) will be interpreted as the title, the rest as the body. In your journal file, the result will look like this:

    2012-03-29 09:00 Called in sick.
    Used the time to clean the house and spent 4h on writing my book.

If you just call `jrnl`, you will be prompted to compose your entry - but you can also configure _jrnl_ to use your external editor.


Installation
------------

Install _jrnl_ using pip:

    pip install jrnl

Or, if you want the option to encrypt your journal,

    pip install jrnl[encrypted]

Alternatively, on OS X with [Homebrew](http://brew.sh/) installed:

    brew install jrnl
