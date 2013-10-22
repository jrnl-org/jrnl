.. _export:

Import and Export
=================


Tag export
----------

With::

    jrnl --tags

you'll get a list of all tags you used in your journal, sorted by most frequent. Tags occurring several times in the same entry are only counted as one.

JSON export
-----------

Can do::

    jrnl --export json

Why not create a beautiful [timeline](http://timeline.verite.co/) of your journal?

Markdown export
---------------

Use::

    jrnl --export markdown

or::

    jrnl --export md

Markdown is a simple markup language that is human readable and can be used to be rendered to other formats (html, pdf). This README for example is formatted in markdown and github makes it look nice.

Text export
-----------

::

    jrnl --export text

or ::

    jrnl --export txt

Pretty-prints your entire journal.

Export to files
---------------

You can specify the output file of your exported journal using the `-o` argument::

    jrnl --export md -o journal.md

The above command will generate a file named `journal.md`. If the `-o` argument is a directory, jrnl will export each entry into an individual file::

    jrnl --export json -o my_entries/

The contents of `my_entries/` will then look like this:

.. code-block:: output

    my_entries/
    |- 2013_06_03_a-beautiful-day.json
    |- 2013_06_07_dinner-with-gabriel.json
    |- ...
