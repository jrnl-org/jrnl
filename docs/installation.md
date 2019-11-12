# Getting started

## Installation

On OS X, the easiest way to install *jrnl* is using
[Homebrew](http://brew.sh/)

``` sh
brew install jrnl
```

On other platforms, install *jrnl* using pip

``` sh
pip install jrnl
```

The first time you run `jrnl` you will be asked where your journal file
should be created and whether you wish to encrypt it.

## Quickstart

To make a new entry, just type

``` sh
jrnl yesterday: Called in sick. Used the time to clean the house and spent 4h on writing my book.
```

and hit return. `yesterday:` will be interpreted as a time stamp.
Everything until the first sentence mark (`.?!:`) will be interpreted as
the title, the rest as the body. In your journal file, the result will
look like this:

``` output
2012-03-29 09:00 Called in sick.
Used the time to clean the house and spent 4h on writing my book.
```

If you just call `jrnl`, you will be prompted to compose your entry -
but you can also configure *jrnl* to use your external editor.
