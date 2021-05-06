<!-- Copyright (C) 2012-2021 jrnl contributors
     License: https://www.gnu.org/licenses/gpl-3.0.html -->

# Extending jrnl

jrnl can be extended with custom importers and exporters.

Note that custom importers and exporters can be given the same name as a
built-in importer or exporter to override it.

Custom Importers and Exporters are traditional Python packages, and are
installed (into jrnl) simply by installing them so they are available to the
Python interpreter that is running jrnl.

## Entry Class

Both the Importers and the Exporters work on the `Entry` class. Below is a
(selective) description of the class, it's properties and functions:

- **Entry** (class) at `jrnl.Entry.Entry`.
    - **title** (string): a single line that represents a entry's title.
    - **date** (datetime.datetime): the date and time assigned to an entry.
    - **body** (string): the main body of the entry. Can be basically any
      length. *jrnl* assumes no particular structure here.
    - **starred** (boolean): is an entry starred? Presumably, starred entries
      are of particular importance.
    - **tags** (list of strings): the tags attached to an entry. Each tag
      includes the pre-facing "tag symbol".
    - **\_\_init\_\_(journal, date=None, text="", starred=False)**: contractor
      method
        - **journal** (*jrnl.Journal.Journal*): a link to an existing Journal
          class. Mainly used to access it's configuration.
        - **date** (datetime.datetime)
        - **text** (string): assumed to include both the title and the body.
          When the title, body, or tags of an entry are requested, this text
          will the parsed to determine the tree.
        - **starred** (boolean)

Entries also have "advanced" metadata if they are using the DayOne backend, but
we'll ignore that for the purposes of this demo.

## Custom Importer

If you have a (custom) datasource that you want to import into your jrnl
(perhaps like a blog export), you can write a custom importer to do this.

An importer takes the source data, turns it into Entries and then appends those
entries to a Journal. Here is a basic Importer, assumed to be provided with a
nicely formated JSON file:

~~~ python
# pelican\contrib\importer\json_importer.py
import sys

from jrnl import Entry
from jrnl.plugins.base import BaseImporter

__version__ = "1.0.0"

class Importer:
    """JSON Importer for jrnl."""

    names = ["json"]
    version = __version__

    @staticmethod
    def import_(journal, input=None)
        """
        Given a nicely formatted JSON file, will add the
        contained Entries to the journal.
        """
        
        old_count = len(journal.entries)
        if input:
            with open(input, "r", encoding="utf-8") as f:
                data = json.loads(f)
        else:
            try:
                data = sys.stdin.read()
            except KeyboardInterrupt:
                print(
                    "[Entries NOT imported into journal.]",
                    file=sys.stderr,
                )
                sys.exit(0)

        for json_entry in data:
            raw = json_entry["title"] + "/n" + json_entry["body"]
            date = json_entry["date"]
            entry = Entry.Entry(self, date, raw)
            journal.entries.append(entry)

        new_cnt = len(journal.entries)
        print(
            "[{} entries imported to '{}' journal]".format(
                new_cnt - old_cnt, journal.name
            ),
            file=sys.stderr,
        )
~~~

Note that the above is very minimal, doesn't do any error checking, and doesn't
try to import all possible entry metadata.

Some implementation notes:

- The importer class must be named **Importer**, and should sub-class
  **jrnl.plugins.base.BaseImporter**.
- The importer module must be within the **jrnl.contrib.importer** namespace.
- The importer must not have any `__init__.py` files in the base directories.
- The importer must be installed as a Python package available to the same
  Python interpreter running jrnl.
- The importer must expose at least the following the following members:
    - **version** (string): the version of the plugin. Displayed to help the
      user debug their installations.
    - **names** (list of strings): these are the "names" that can be passed to
      the CLI to invole your importer. If you specify one used by a built-in
      plugin, it will overwrite it (effectively making the built-in one
      unavailable).
    - **import_(journal, input=None)**: the actual importer. Must append
      entries to the journal passed to it. It is recommended to accept either a
      filename or standard input as a source.

## Custom Exporter

Custom exporters are useful to make jrnl's data available to other programs.
One common usecase would to generate the input to be used by a static site
generator or blogging engine.

An exporter take either a whole journal or a specific entry and exports it.
Below is a basic JSON Exporter; note that a more extensive JSON exporter is
included in jrnl and so this (if installed) would override the built in
exporter.

~~~ python
# pelican\contrib\exporter\custom_json_exporter.py
import json

from jrnl.plugins.base import BaseExporter

__version__ = "1.0.0"

class Exporter(BaseExporter):
    """
    This basic Exporter can convert entries and journals into JSON.
    """

    names = ["json"]
    extension = "json"
    version = __version__

    @classmethod
    def entry_to_dict(cls, entry):
        return = {
            "title": entry.title,
            "body": entry.body,
            "date": entry.date.strftime("%Y-%m-%d"),
        }

    @classmethod
    def export_entry(cls, entry):
        """Returns a json representation of a single entry."""
        return json.dumps(cls.entry_to_dict(entry), indent=2) + "\n"

    @classmethod
    def export_journal(cls, journal):
        """Returns a json representation of an entire journal."""
        tags = get_tags_count(journal)
        result = {
            "entries": [
                cls.entry_to_dict(e) for e in journal.entries
            ],
        }
        return json.dumps(result, indent=2)
~~~

Note that the above is very minimal, doesn't do any error checking, and doesn't
export all entry metadata.

Some implementation notes:

- the exporter class must be named **Exporter** and should sub-class
  **jrnl.plugins.base.BaseExporter**.
- the exporter module must be within the **jrnl.contrib.exporter** namespace.
- The exporter must not have any `__init__.py` files in the base directories.
- The exporter must be installed as a Python package available to the same
  Python interpreter running jrnl.
- the exporter should expose at least the following the following members
  (there are a few more you will need to define if you don't subclass
  `jrnl.plugins.exporter.text_exporter`):
    - **version** (string): the version of the plugin. Displayed to help the
      user debug their installations.
    - **names** (list of strings): these are the "names" that can be passed to
      the CLI to invole your exporter. If you specific one used by a built-in
      plugin, it will overwrite it (effectively making the built-in one
      unavailable).
    - **extension** (string): the file extention used on exported entries.
    - **export_entry(entry)**: given an entry, returns a string of the formatted,
      exported entry.
    - **export_journal(journal)**: given a journal, returns a string of the
      formatted, exported entries of the journal.

## Development Tips

- editable installs (`pip install -e ...`) don't seem to play nice with
  the namespace layout. If your plugin isn't appearing, try a non-editable
  install of both jrnl and your plugin.
