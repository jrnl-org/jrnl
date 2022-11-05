<!--
Copyright © 2012-2022 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# Advanced Usage

## Configuration File

`jrnl` has a wide variety of options that can be customized through the config file,
including templates, formats, multiple journals, and more. See
the [configuration file reference](./reference-config-file.md) for details
or read on for some common use cases.

### Multiple journal files

You can configure `jrnl`to use with multiple journals (eg.
`private` and `work`) by defining more journals in your [config file](./reference-config-file.md),
for example:

``` yaml
journals:
  default: ~\journal.txt
  work: ~\work.txt
```

The `default` journal gets created the first time you start `jrnl`
Now you can access the `work` journal by using `jrnl work` instead of
`jrnl`, eg.

``` sh
jrnl work at 10am: Meeting with @Steve
jrnl work -n 3
```

will both use `~/work.txt`, while `jrnl -n 3` will display the last
three entries from `~/journal.txt` (and so does `jrnl default -n 3`).

You can also override the default options for each individual journal.
If your `jrnl.yaml` looks like this:

``` yaml
encrypt: false
journals:
default: ~/journal.txt
work:
  journal: ~/work.txt
  encrypt: true
food: ~/my_recipes.txt
```

Your `default` and your `food` journals won't be encrypted, however your
`work` journal will!

You can override all options that are present at
the top level of `jrnl.yaml`, just make sure that at the very least
you specify a `journal: ...` key that points to the journal file of
that journal.

Consider the following example configuration

```yaml
editor: vi -c startinsert 
journals: 
  default: ~/journal.txt 
  work: 
    journal: ~/work.txt 
    encrypt: true 
    display_format: json 
    editor: code -rw 
  food:
    display_format: markdown 
    journal: ~/recipes.txt 
```

The `work` journal is encrypted, prints to `json` by default, and is edited using an existing window of VSCode. Similarly, the `food` journal prints to markdown by default, but uses all the other defaults.

### Modifying Configurations from the Command line 

You can override a configuration field for the current instance of `jrnl` using `--config-override CONFIG_KEY CONFIG_VALUE` where `CONFIG_KEY` is a valid configuration field, specified in dot notation and `CONFIG_VALUE` is the (valid) desired override value. The dot notation can be used to change config keys within other keys, such as `colors.title` for the `title` key within the `colors` key.

You can specify multiple overrides as multiple calls to `--config-override`.
!!! note
    These overrides allow you to modify ***any*** field of your jrnl configuration. We trust that you know what you are doing. 

#### Examples: 

``` sh
#Create an entry using the `stdin` prompt, for rapid logging
jrnl --config-override editor ""

#Populate a project's log
jrnl --config-override journals.todo "$(git rev-parse --show-toplevel)/todo.txt" todo find my towel 

#Pass multiple overrides 
jrnl --config-override display_format fancy --config-override linewrap 20 \
--config-override colors.title green

```

### Using an alternate config

You can specify an alternate configuration file for the current instance of `jrnl` using `--config-file CONFIG_FILE_PATH` where
`CONFIG_FILE_PATH` is a path to an alternate `jrnl` configuration file. 

#### Examples:

```
# Use personalised configuration file for personal journal entries
jrnl --config-file ~/foo/jrnl/personal-config.yaml

# Use alternate configuration file for work-related entries
jrnl --config-file ~/foo/jrnl/work-config.yaml

# Use default configuration file (created on first run)
jrnl
```
