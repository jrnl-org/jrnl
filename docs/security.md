# Privacy and Security

`jrnl` is designed with privacy and security in mind, but there are some
limitations to be aware of.

## Password strength

`jrnl` doesn't enforce password strength requirements. Short or commonly-used
passwords can easily be circumvented by someone with basic security skills
and access to your encrypted `jrnl` file.

## Shell history

Since you can enter entries from the command line, any tool
that logs command line actions is a potential security risk. See
below for how to deal with this problem in various shells.

### bash

You can disable history logging for jrnl in your `.bashrc`:

``` sh
HISTIGNORE="$HISTIGNORE:jrnl *"
```

### zsh

Disable history logging by adding this to your `zshrc`:

``` sh
setopt HIST_IGNORE_SPACE
alias jrnl=" jrnl"
```

### fish

Add this abbreviation to your `fish` configuration to run jrnl with
a space before it, which prevents `fish` from logging it:

``` sh
abbr --add jrnl " jrnl"
```

To delete existing `jrnl` commands from `fish`’s history, run
`history delete --prefix 'jrnl '`.

### Windows Command Prompt

Windows doesn't log history to disk, but it does keep it in your command
prompt session. Close the command prompt or press Alt+F7 to clear its
history after journaling.

## Files in transit from editor to jrnl

When creating or editing an entry, `jrnl` uses a plain text temporary file on disk
to give your editor access to it. `jrnl` deletes the temporary file when it
saves the entry back to your journal.

If you save an entry but haven't closed your editor yet, and your computer shuts
off or the `jrnl` process is killed, the entry remains on your disk as a
temporary file. You can mitigate this issue by only saving with your editor
right before closing it.

## Plausible deniability

You may be able to hide the contents of your journal behind a layer of encryption,
but if someone has access to your configuration file, then they can figure out that
you have a journal, where that journal file is, and when you last edited it.
With a sufficient power imbalance, an attacker may be able to force you to unencrypt
it through legal means or other forms of coercion.

## Notice any other risks?

Please let the maintainers know by [filing an issue on GitHub](https://github.com/jrnl-org/jrnl/issues).