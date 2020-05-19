# Overview

`jrnl` is a simple but powerful plain text journal application for the command
line.

Your imagination may be limitless, but your memory probably isn't. `jrnl` lets
you write something down, and then it gets out of the way.

## how it works

New entries are created on the command line:

``` sh
jrnl today at 8am: I arrived at work to find a birthday present on my desk. My colleagues are the best!
```

Support for external editors is included.

### one file type to rule them all...

`jrnl` stores your journals as human-readable, future-proof plain text files.
You can store them wherever you want, including in shared folders to keep them
synchronized between devices. And because journal files are stored as plain
text, you can rest assured that your journals will be readable for centuries.

### ...and as many files as you need
  
`jrnl` allows you to work with multiple journals, each of which is stored as a
single file using date and time tags to identify individual entries. `jrnl`
makes it easy to find the entries you want, and only the ones you want, so that
you can read them or edit them. Here's an example: say you want to find all of
the entries you wrote on January 3rd, 2020 that include the word _cat_, and
change every instance of the word _cat_ to _dog_? Easy:

``` sh
jrnl -on 2020-01-03 -contains 'cat' --edit
```

### for your eyes only
  
To protect your journal, you can encrypt it using [256-bit AES encryption](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard).