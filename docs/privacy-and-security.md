<!--
Copyright © 2012-2023 jrnl contributors
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

## Editor history

Some editors keep usage history stored on disk for future use. This can be a
security risk in the sense that sensitive information can leak via recent
search patterns or editor commands.

### Vim

Vim stores progress data in a so called Viminfo file located at `~/.viminfo`
which contains all sorts of user data including command line history, search
string history, search/substitute patterns, contents of register etc. Also to
be able to recover opened files after an unexpected application close Vim uses
swap files.

These options as well as other leaky features can be disabled by setting the
`editor` key in the Jrnl settings like this:

``` yaml
editor: "vim -c 'set viminfo= noswapfile noundofile nobackup nowritebackup noshelltemp history=0 nomodeline secure'"
```

To disable all plugins and custom configurations and start Vim with the default
configuration `-u NONE` can be passed on the command line as well. This will
ensure that any rouge plugins or other difficult to catch information leaks are
eliminated. The downside to this is that the editor experience will decrease
quite a bit.

To instead let Vim automatically detect when a Jrnl file is being edited an
autocommand can be used. Place this in your `~/.vimrc`:

``` vim
autocmd BufNewFile,BufReadPre *.jrnl setlocal viminfo= noswapfile noundofile nobackup nowritebackup noshelltemp history=0 nomodeline secure
```

Please see `:h <option>` in Vim for more information about the options mentioned.

### Neovim

Neovim strives to be mostly compatible with Vim and has therefore similar
functionality as Vim. One difference in Neovim is that the Viminfo file is
instead called the ShaDa ("shared data") file which resides in
`~/.local/state/nvim` (`~/.local/share/nvim` pre Neovim v0.8.0). The ShaDa file
can be disabled in the same way as for Vim.

``` yaml
editor: "nvim -c 'set shada= noswapfile noundofile nobackup nowritebackup noshelltemp history=0 nomodeline secure'"
```

`-u NONE` can be passed here as well to start a session with the default configs.

As for Vim above we can create an autocommand in Vimscript:

``` vim
autocmd BufNewFile,BufReadPre *.jrnl setlocal shada= noswapfile noundofile nobackup nowritebackup noshelltemp history=0 nomodeline secure
```

or the same but in Lua:

``` lua
vim.api.nvim_create_autocmd( {"BufNewFile","BufReadPre" }, {
  group = vim.api.nvim_create_augroup("PrivateJrnl", {}),
  pattern = "*.jrnl",
  callback = function()
    vim.o.shada = ""
    vim.o.swapfile = false
    vim.o.undofile = false
    vim.o.backup = false
    vim.o.writebackup = false
    vim.o.shelltemp = false
    vim.o.history = 0
    vim.o.modeline = false
    vim.o.secure = true
  end,
})
```

Please see `:h <option>` in Neovim for more information about the options mentioned.

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
