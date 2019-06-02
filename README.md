jrnl [![Backers on Open Collective](https://opencollective.com/jrnl/backers/badge.svg)](#backers) [![Sponsors on Open Collective](https://opencollective.com/jrnl/sponsors/badge.svg)](#sponsors) [![Build Status](http://img.shields.io/travis/maebert/jrnl.svg?style=flat)](https://travis-ci.org/maebert/jrnl)  [![Downloads](https://pepy.tech/badge/jrnl)](https://pepy.tech/project/jrnl) [![Version](http://img.shields.io/pypi/v/jrnl.svg?style=flat)](https://pypi.python.org/pypi/jrnl/)
====

_For news on updates or to get help, [read the docs](http://maebert.github.io/jrnl/overview.html), follow [@maebert](https://twitter.com/maebert) or [submit an issue](https://github.com/maebert/jrnl/issues/new) on Github._

*jrnl* is a simple journal application for your command line. Journals are stored as human readable plain text files - you can put them into a Dropbox folder for instant syncing and you can be assured that your journal will still be readable in 2050, when all your fancy iPad journal applications will long be forgotten.

*jrnl* also plays nice with the fabulous [DayOne](http://dayoneapp.com/) and can read and write directly from and to DayOne Journals.

Optionally, your journal can be encrypted using the [256-bit AES](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard).

### Why keep a journal?

Journals aren't just for angsty teenagers and people who have too much time on their summer vacation. A journal helps you to keep track of the things you get done and how you did them. Your imagination may be limitless, but your memory isn't. For personal use, make it a good habit to write at least 20 words a day. Just to reflect what made this day special, why you haven't wasted it. For professional use, consider a text-based journal to be the perfect complement to your GTD todo list - a documentation of what and how you've done it.

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

## Contributors

This project exists thanks to all the people who contribute. [[Contribute](CONTRIBUTING.md)].
<a href="https://github.com/maebert/jrnl/graphs/contributors"><img src="https://opencollective.com/jrnl/contributors.svg?width=890&button=false" /></a>


## Backers

Thank you to all our backers! 🙏 [[Become a backer](https://opencollective.com/jrnl#backer)]

<a href="https://opencollective.com/jrnl#backers" target="_blank"><img src="https://opencollective.com/jrnl/backers.svg?width=890"></a>


## Sponsors

Support this project by becoming a sponsor. Your logo will show up here with a link to your website. [[Become a sponsor](https://opencollective.com/jrnl#sponsor)]

<a href="https://opencollective.com/jrnl/sponsor/0/website" target="_blank"><img src="https://opencollective.com/jrnl/sponsor/0/avatar.svg"></a>
<a href="https://opencollective.com/jrnl/sponsor/1/website" target="_blank"><img src="https://opencollective.com/jrnl/sponsor/1/avatar.svg"></a>
<a href="https://opencollective.com/jrnl/sponsor/2/website" target="_blank"><img src="https://opencollective.com/jrnl/sponsor/2/avatar.svg"></a>
<a href="https://opencollective.com/jrnl/sponsor/3/website" target="_blank"><img src="https://opencollective.com/jrnl/sponsor/3/avatar.svg"></a>
<a href="https://opencollective.com/jrnl/sponsor/4/website" target="_blank"><img src="https://opencollective.com/jrnl/sponsor/4/avatar.svg"></a>
<a href="https://opencollective.com/jrnl/sponsor/5/website" target="_blank"><img src="https://opencollective.com/jrnl/sponsor/5/avatar.svg"></a>
<a href="https://opencollective.com/jrnl/sponsor/6/website" target="_blank"><img src="https://opencollective.com/jrnl/sponsor/6/avatar.svg"></a>
<a href="https://opencollective.com/jrnl/sponsor/7/website" target="_blank"><img src="https://opencollective.com/jrnl/sponsor/7/avatar.svg"></a>
<a href="https://opencollective.com/jrnl/sponsor/8/website" target="_blank"><img src="https://opencollective.com/jrnl/sponsor/8/avatar.svg"></a>
<a href="https://opencollective.com/jrnl/sponsor/9/website" target="_blank"><img src="https://opencollective.com/jrnl/sponsor/9/avatar.svg"></a>


