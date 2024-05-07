<!--
Copyright © 2012-2023 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# Getting started

## Installation

On Mac and Linux, the easiest way to install `jrnl` is using
[Homebrew](http://brew.sh/):

``` sh
brew install jrnl
```

On other platforms, install `jrnl` using [Python](https://www.python.org/) 3.10+ and [pipx](https://pipxproject.github.io/pipx/):

``` sh
pipx install jrnl
```

!!! tip
     Do not use `sudo` while installing `jrnl`. This may lead to path issues.

The first time you run `jrnl` you will be asked where your journal file
should be created and whether you wish to encrypt it.

## Quickstart

To make a new entry, just type

``` text
jrnl yesterday: Called in sick. Used the time to clean, and spent 4h on writing my book.
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
but you can also [configure](advanced.md) *jrnl* to use your external editor.
