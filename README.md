jrnl [![Build Status](https://travis-ci.com/jrnl-org/jrnl.svg?branch=master)](https://travis-ci.com/jrnl-org/jrnl) [![Downloads](https://pepy.tech/badge/jrnl)](https://pepy.tech/project/jrnl) [![Version](http://img.shields.io/pypi/v/jrnl.svg?style=flat)](https://pypi.python.org/pypi/jrnl/)
====

_To get help, [submit an issue](https://github.com/jrnl-org/jrnl/issues/new) on
Github._

*jrnl* is a simple journal application for your command line. Journals are
stored as human readable plain text files - you can put them into a Dropbox
folder for instant syncing and you can be assured that your journal will still
be readable in 2050, when all your fancy iPad journal applications will long be
forgotten.

Optionally, your journal can be encrypted using the [256-bit
AES](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard).

### Why keep a journal?

Journals aren't just for people who have too much time on their summer
vacation. A journal helps you to keep track of the things you get done and how
you did them. Your imagination may be limitless, but your memory isn't. For
personal use, make it a good habit to write at least 20 words a day. Just to
reflect what made this day special, or why you haven't wasted it. For
professional use, consider a text-based journal to be the perfect complement to
your GTD todo list - a documentation of what and how you've done it.

In a Nutshell
-------------

To make a new entry, just type

    jrnl yesterday: Called in sick. Used the time cleaning the house and writing my book.

and hit return. `yesterday:` will be interpreted as a timestamp. Everything
until the first sentence mark (`.?!`) will be interpreted as the title, the
rest as the body. In your journal file, the result will look like this:

    [2012-03-29 09:00] Called in sick.
    Used the time cleaning the house and writing my book.

If you just call `jrnl`, you will be prompted to compose your entry - but you
can also configure _jrnl_ to use your external editor.

For more information, please read our [documentation](https://jrnl.sh/overview/).

## Contributors

### Maintainers
Our maintainers help keep the lights on for the project. Please thank them if
you like jrnl.
 * Jonathan Wren ([wren](https://github.com/wren))
 * Micah Ellison ([micahellison](https://github.com/micahellison))

### Code Contributors
This project is made with love by the many fabulous people who have
contributed. Jrnl couldn't exist without each and every one of you!

<a href="https://github.com/jrnl-org/jrnl/graphs/contributors"><img
src="https://opencollective.com/jrnl/contributors.svg?width=890&button=false"
/></a>

If you'd also like to help make jrnl better, please see our [contributing
documentation](CONTRIBUTING.md).

### Financial Backers

Another way show support is through direct financial contributions. These funds
go to covering our costs, and are a quick way to show your appreciation for
jrnl.

[Become a financial contributor](https://opencollective.com/jrnl/contribute)
and help us sustain our community.

<a href="https://opencollective.com/jrnl"><img
src="https://opencollective.com/jrnl/individuals.svg?width=890"></a>
