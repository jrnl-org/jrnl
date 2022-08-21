<!--
Copyright © 2012-2022 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# Privacy and Security

`jrnl` is designed with privacy and security in mind, but like any other
program there are some limitations to be aware of.

## Password strength

`jrnl` doesn't enforce password strength requirements. Short or commonly-used
passwords can be easily circumvented by someone with basic security skills
to access to your encrypted `jrnl` file.

## Shell history

Since you can enter entries from the command line, any tool that logs command
line actions is a potential security risk. See below for how to deal with this
problem in various shells.

### bash

You can disable history logging for jrnl by adding this line into your
`~/.bashrc` file:

``` sh
HISTIGNORE="$HISTIGNORE:jrnl *"
```

To delete existing `jrnl` commands from `bash` history, simply delete them from
your bash history file. The default location of this file is `~/.bash_history`,
but you can run `echo "$HISTFILE"` to find it if needed.  Also, you can run
`history -c` to delete all commands from your history.

### zsh

You can disable history logging for jrnl by adding this to your `~/.zshrc`
file:

``` sh
setopt HIST_IGNORE_SPACE
alias jrnl=" jrnl"
```

To delete existing `jrnl` commands from `zsh` history, simply remove them from
your zsh history file. The default location of this file is `~/.zsh_history`,
but you can run `echo "$HISTFILE"` to find it if needed. Also, you can run
`history -c` to delete all commands from your history.

### fish

By default `fish` will not log any command that starts with a space. If you
want to always run jrnl with a space before it, then you can add this to your
`~/.config/fish/config.fish` file:

``` sh
abbr --add jrnl " jrnl"
```

To delete existing jrnl commands from `fish` history, run `history delete --prefix 'jrnl '`.

### Windows Command Prompt

Windows doesn't log history to disk, but it does keep it in your command prompt
session. Close the command prompt or press `Alt`+`F7` to clear your history
after journaling.

## Files in transit from editor to jrnl

When creating or editing an entry, `jrnl` uses a unencrypted temporary file on
disk in order to give your editor access to your journal. After you close your
editor, `jrnl` then deletes this temporary file.

So, if you have saved a journal entry but haven't closed your editor yet, the
unencrypted temporary remains on your disk. If your computer were to shut off
during this time, or the `jrnl` process were killed unexpectedly, then the
unencrypted temporary file will remain on your disk. You can mitigate this
issue by only saving with your editor right before closing it. You can also
manually delete these files (i.e. files named `jrnl_*.txt`) from your temporary
folder.

## Plausible deniability

You may be able to hide the contents of your journal behind a layer of encryption,
but if someone has access to your configuration file, then they can figure out that
you have a journal, where that journal file is, and when you last edited it.
With a sufficient power imbalance, someone may be able to force you to unencrypt
it through non-technical means.

## Saved Passwords

When creating an encrypted journal, you'll be prompted as to whether or not you
want to "store the password in your keychain." This keychain is accessed using
the [Python keyring library](https://pypi.org/project/keyring/), which has different
behavior depending on your operating system.

In Windows, the keychain is the Windows Credential Manager (WCM), which can't be locked
and can be accessed by any other application running under your username. If this is
a concern for you, you may not want to store your password.


## Notice any other risks?

Please let the maintainers know by [filing an issue on GitHub](https://github.com/jrnl-org/jrnl/issues).
