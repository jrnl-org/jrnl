<!-- Copyright (C) 2012-2021 jrnl contributors
     License: https://www.gnu.org/licenses/gpl-3.0.html -->

# Creating Importer and Exporter Plugins

You can extend `jrnl` with custom importer and exporter plugins. Importer
plugins add new ways to import data into `jrnl`, while exporter plugins add
new ways to change the output of `jrnl`, whether to make data available to
other programs or just view entries differently in the console.

Both types of plugins use
[native namespace packages](https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages).
Once they are installed, they should be available to jrnl when using the
same Python interpreter that was used to install them.

!!! tip
    To confirm that a plugin is present, run `jrnl --diagnostic`

## Getting Started

Before you start working on a plugin, it's good to have a basic understanding
of [Python packaging](https://packaging.python.org/guides/) and namespace
packages in particular.

You can find sample plugins in the `/tests/external_plugins_src/` directory of
the [jrnl source](https://github.com/jrnl-org/jrnl).

## Understanding the Entry Class

Importer and exporter plugins work on the `Entry` class, which is
responsible for representing the data in a journal entry. Plugins will
generally access the following properties and functions of this class:

  - **title** (string): a single line that represents a entry's title.
  - **date** (datetime.datetime): the date and time assigned to an entry.
  - **body** (string): the main body of the entry. Can be any length.
      `jrnl` assumes no particular structure here.
  - **starred** (boolean): true if an entry is "starred"
  - **tags** (list of strings): the tags attached to an entry. Each tag
    includes the pre-facing "tag symbol" which defaults to `@`.
  - **\_\_init\_\_(journal, date=None, text="", starred=False)**: constructor for new entries
      - **journal** (*jrnl.Journal.Journal*): a link to an existing Journal
        class. Mainly used to access its configuration.
      - **date** (datetime.datetime): the date of the entry
      - **text** (string): includes the entry's title and its body if one is included.
        When the title, body, or tags of an entry are requested, this text
        will the parsed to determine the tree.
      - **starred** (boolean)

!!! warning
    The Entry class is likely to change in future versions of journal. In
    particular, there may be a unique identifier added to it. Also, when
    using the DayOne backend, entries have additional metadata, including
    a "uuid" unique identifier.

## Creating an Importer Plugin

An importer takes source data, turns it into Entries and then appends those
entries to a Journal.

### Structure

- The importer class must be named **Importer**, and should sub-class
  **jrnl.plugins.base.BaseImporter**.
- The importer module must be within the **jrnl.contrib.importer** namespace.
- The importer must not have any `__init__.py` files in the base directories
  (but you can have one for your importer base directory if it is in a
  directory rather than a single file).
- The importer must expose at least the following the following members:
    - **version** (string): the version of the plugin. Displayed to help the
      user debug their installations.
    - **names** (list of strings): these are the "names" that can be passed to
      the CLI to involve your importer. If you specify one used by a built-in
      plugin, it will overwrite it (effectively making the built-in one
      unavailable).
    - **import_(journal, input=None)**: the actual importer. Must append
      entries to the journal passed to it. It is recommended to accept either a
      filename or standard input as a source.

### Importer Example

You can find a basic Importer plugin in the `jrnl`
[source](https://github.com/jrnl-org/jrnl) at
`/tests/external_plugins_src/jrnl/contrib/importer/simple_json.py`. The
sample plugin assumes that it will be provided with a nicely formatted JSON
file.

!!! warning
    This sample code is very minimal, doesn't do any error checking, and doesn't
    try to import all possible entry metadata.

### Use Cases

Another potential use of a custom importer is to effectively create a scripted
entry creator. For example, maybe each day you want to create a journal entry
that contains the answers to specific questions; you could create a custom
"importer" that would ask you the questions, and then create an entry containing
the answers provided.

## Creating an Exporter Plugin

An exporter takes either a whole journal or a specific entry and exports it.

### Structure

- The exporter class must be named **Exporter** and should sub-class
  **jrnl.plugins.base.BaseExporter**.
- The exporter module must be within the **jrnl.contrib.exporter** namespace.
- The exporter must not have any `__init__.py` files in the base directories
  (but you can have one for your exporter base directory if it is in a
  directory rather than a single file).
- The exporter should expose at least the following the following members
  (there are a few more you will need to define if you don't subclass
  `jrnl.plugins.base.BaseExporter`):
    - **version** (string): the version of the plugin. Displayed to help the
      user debug their installations.
    - **names** (list of strings): these are the "names" that can be passed to
      the CLI to invole your exporter. If you specific one used by a built-in
      plugin, it will overwrite it (effectively making the built-in one
      unavailable).
    - **extension** (string): the file extention used on exported entries.
    - **export_entry(entry)**: given an entry, returns a string of the formatted,
      exported entry.
    - **export_journal(journal)**: (optional) given a journal, returns a string
      of the formatted, exported entries of the journal. If not implemented,
      `jrnl` will call **export_entry()** on each entry in turn and then
      concatenate the results together.

### Exporter Example

You can find a basic Exporter plugin in the `jrnl`
[source](https://github.com/jrnl-org/jrnl) at
`/tests/external_plugins_src/jrnl/contrib/exporter/custom_json.py`.

Note that a more extensive JSON exporter is
included in `jrnl` and so this (if installed) would override the built in
exporter.

!!! warning
    The above is very minimal, doesn't do any error checking, and doesn't
    export all entry metadata.


### Special Exporters

There are a few "special" exporters, in that they are called by `jrnl` in
situations other than a traditional export. They are:

- **short** -- called by `jrnl --short`. Displays each entry on a single line.
  The default is to print the timestamp of the entry, followed by the title.
  The built-in (default) plugin is at `jrnl.plugins.exporter.short`.
- **default** -- called when a different format is not specified. The built-in
  (default) plugin is at `jrnl.plugins.exporter.pretty`.

## Development Tips

- Editable installs (`pip install -e ...`) don't seem to play nice with
  the namespace layout. If your plugin isn't appearing, try a non-editable
  install of both `jrnl` and your plugin.
- If you run `jrnl` from the main project root directory (the one that contains
  `jrnl`'s source code), namespace plugins won't be recognized. This is (I
  suspect) because the Python interpreter will find your `jrnl` source directory
  (which doesn't contain your namespace plugins) before it find your
  "site-packages" directory (i.e. installed packages, which will recognize
  namespace packages).
- Don't name your plugin file "testing.py" or it won't be installed (at least
  automatically) by pip.
- For examples, you can look to the `jrnl`'s internal importers and exporters.
  As well, there are some basic external examples included in `jrnl`'s git repo
  at `tests/external_plugins_src` (including the example code above).
- Custom importers and exporters can be given the same name as a built-in importer
  or exporter to override it.
