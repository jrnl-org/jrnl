jrnl
====

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

Alternatively, install manually by cloning the repository:

    git clone git://github.com/maebert/jrnl.git
    cd jrnl
    python setup.py install

The first time you run `jrnl` you will be asked where your journal file should be created and whether you wish to encrypt it.

Usage
-----

_jrnl_ has two modes: __composing__ and __viewing__.

### Viewing:

    jrnl -n 10

will list you the ten latest entries,

    jrnl -from "last year" -to march

everything that happened from the start of last year to the start of last march. If you only want to see the titles of your entries, use

    jrnl -short

### Using Tags:

Keep track of people, projects or locations, by tagging them with an `@` in your entries:

    jrnl Had a wonderful day on the @beach with @Tom and @Anna.

You can filter your journal entries just like this:

    jrnl @pinkie @WorldDomination

Will print all entries in which either `@pinkie` or `@WorldDomination` occurred.

    jrnl -n 5 -and @pineapple @lubricant

the last five entries containing both `@pineapple` __and__ `@lubricant`. You can change which symbols you'd like to use for tagging in the configuration.

> __Note:__ `jrnl @pinkie @WorldDomination` will switch to viewing mode because although _no_ command line arguments are given, all the input strings look like tags - _jrnl_ will assume you want to filter by tag.

### Composing:

Composing mode is entered by either starting `jrnl` without any arguments -- which will prompt you to write an entry or launch your editor -- or by just writing an entry on the prompt, such as

    jrnl today at 3am: I just met Steve Buscemi in a bar! He looked funny.


### Smart timestamps:

Timestamps that work:

* at 6am
* yesterday
* last monday
* sunday at noon
* 2 march 2012
* 7 apr
* 5/20/1998 at 23:42

Import and export
-----------------

### Tag export

With

    jrnl --tags

you'll get a list of all tags you used in your journal, sorted by most frequent. Tags occuring several times in the same entry are only counted as one.

### JSON export

Can do:

    jrnl --json

Why not create a beautiful [timeline](http://timeline.verite.co/) of your journal?

### Markdown export

    jrnl --markdown

Markdown is a simple markup language that is human readable and can be used to be rendered to other formats (html, pdf). This README for example is formatted in markdown and github makes it look nice.

Encryption
----------

If you don't choose to encrypt your file when you run `jrnl` for the first time, you can encrypt your existing journal file or change its password using

    jrnl --encrypt

If it is already encrypted, you will first be asked for the current password. You can then enter a new password and your plain journal will replaced by the encrypted file. Conversely,

    jrnl --decrypt

will replace your encrypted journal file by a Journal in plain text. You can also specify a filename, ie. `jrnl --decrypt plain_text_copy.txt`, to leave your original file untouched.


Advanced usages
--------------

The first time launched, _jrnl_ will create a file called `.jrnl_config` in your home directory.

### .jrnl_config

The configuration file is a simple JSON file with the following options.

- `journals`: paths to your journal files
- `editor`: if set, executes this command to launch an external editor for writing your entries, e.g. `vim` or `subl -w` (note the `-w` flag to make sure _jrnl_ waits for Sublime Text to close the file before writing into the journal).
- `encrypt`: if `true`, encrypts your journal using AES.
- `password`: you may store the password you used to encrypt your journal in plaintext here. This is useful if your journal file lives in an unsecure space (ie. your Dropbox), but the config file itself is more or less safe.
- `tagsymbols`: Symbols to be interpreted as tags. (__See note below__)
- `default_hour` and `default_minute`: if you supply a date, such as `last thursday`, but no specific time, the entry will be created at this time
- `timeformat`: how to format the timestamps in your journal, see the [python docs](http://docs.python.org/library/time.html#time.strftime) for reference
- `highlight`: if `true`, tags will be highlighted in cyan.
- `linewrap`: controls the width of the output. Set to `0` or `false` if you don't want to wrap long lines.

> __Note on `tagsymbols`:__ Although it seems intuitive to use the `#` character for tags, there's a drawback: on most shells, this is interpreted as a meta-character starting a comment. This means that if you type
>
>     jrnl Implemented endless scrolling on the #frontend of our website.
>
> your bash will chop off everything after the `#` before passing it to _jrnl_). To avoid this, wrap your input into quotation marks like this:
>
>     jrnl "Implemented endless scrolling on the #frontend of our website."
>
> Or use the built-in prompt or an external editor to compose your entries.

### DayOne Integration

Using your DayOne journal instead of a flat text file is dead simple - instead of pointing to a text file, set the `"journal"` key in your `.jrnl_conf` to point to your DayOne journal. This is a folder ending with `.dayone`, and it's located at

    * `~/Library/Application Support/Day One/` by default
    * `~/Dropbox/Apps/Day One/` if you're syncing with Dropbox and
    * `~/Library/Mobile Documents/5U8NS4GX82~com~dayoneapp~dayone/Documents/` if you're syncing with iCloud.

Instead of all entries being in a single file, each entry will live in a separate `plist` file. You can also star entries when you write them:

    jrnl -star yesterday: Lunch with @Arthur

### Multiple journal files

You can configure _jrnl_ to use with multiple journals (eg. `private` and `work`) by defining more journals in your `.jrnl_config`, for example:

    "journals": {
      "default": "~/journal.txt",
      "work":    "~/work.txt"
    },

The `default` journal gets created the first time you start _jrnl_. Now you can access the `work` journal by using `jrnl work` instead of `jrnl`, eg.

    jrnl work at 10am: Meeting with @Steve
    jrnl work -n 3

will both use `~/work.txt`, while `jrnl -n 3` will display the last three entries from `~/journal.txt` (and so does `jrnl default -n 3`).

You can also override the default options for each individual journal. If you `.jrnl_conf` looks like this:

    {
      ...
      "encrypt": false
      "journals": {
        "default": "~/journal.txt",
        "work": {
          "journal": "~/work.txt",
          "encrypt": true
        },
        "food": "~/my_recipes.txt",
    }

Your `default` and your `food` journals won't be encrypted, however your `work` journal will! You can override all options that are present at the top level of `.jrnl_conf`, just make sure that at the very least you specify a `"journal": ...` key that points to the journal file of that journal.

### Manual decryption

Should you ever want to decrypt your journal manually, you can do so with any program that supports the AES algorithm. The key used for encryption is the SHA-256-hash of your password, and the IV (initialisation vector) is stored in the first 16 bytes of the encrypted file. So, to decrypt a journal file in python, run

    import hashlib, Crypto.Cipher
    key = hashlib.sha256(my_password).digest()
    with open("my_journal.txt") as f:
        cipher = f.read()
        crypto = AES.new(key, AES.MODE_CBC, iv = cipher[:16])
        plain = crypto.decrypt(cipher[16:])

Known Issues
------------

- The Windows shell prior to Windows 7 has issues with unicode encoding. If you want to use non-ascii characters, change the codepage with `chcp 1252` before using `jrnl` (Thanks to Yves Pouplard for solving this!)
- _jrnl_ relies on the `PyCrypto` package to encrypt journals, which has some known problems with installing within virtual environments. If you want to install __jrnl__ within a virtual environment, you need to [install PyCyrypto manually](https://www.dlitz.net/software/pycrypto/) first.

