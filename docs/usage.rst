.. _usage:

Basic Usage
===========

*jrnl* has two modes: **composing** and **viewing**. Basically, whenever you `don't` supply any arguments that start with a dash or double-dash, you're in composing mode, meaning you can write your entry on the command line or an editor of your choice.

We intentionally break a convention on command line arguments: all arguments starting with a `single dash` will `filter` your journal before viewing it, and can be combined arbitrarily. Arguments with a `double dash` will control how your journal is displayed or exported and are mutually exclusive (ie. you can only specify one way to display or export your journal at a time).


Composing Entries
-----------------

Composing mode is entered by either starting ``jrnl`` without any arguments -- which will prompt you to write an entry or launch your editor -- or by just writing an entry on the prompt, such as::

    jrnl today at 3am: I just met Steve Buscemi in a bar! He looked funny.

You can also import an entry directly from a file::

    jrnl < my_entry.txt

Smart timestamps
~~~~~~~~~~~~~~~~

Timestamps that work:

* at 6am
* yesterday
* last monday
* sunday at noon
* 2 march 2012
* 7 apr
* 5/20/1998 at 23:42

Starring entries
~~~~~~~~~~~~~~~~

To mark an entry as a favourite, simply "star" it::

    jrnl last sunday *: Best day of my life.

If you don't want to add a date (ie. your entry will be dated as now), The following options are equivalent:

* ``jrnl *: Best day of my life.``
* ``jrnl *Best day of my life.``
* ``jrnl Best day of my life.*``

.. note::

  Just make sure that the asterisk sign is **not** surrounded by whitespaces, e.g. ``jrnl Best day of my life! *`` will **not** work (the reason being that the ``*`` sign has a special meaning on most shells).

Viewing
-------

::

    jrnl -n 10

will list you the ten latest entries, ::

    jrnl -from "last year" -until march

everything that happened from the start of last year to the start of last march. To only see your favourite entries, use ::

    jrnl -starred

Using Tags
----------

Keep track of people, projects or locations, by tagging them with an ``@`` in your entries ::

    jrnl Had a wonderful day on the @beach with @Tom and @Anna.

You can filter your journal entries just like this: ::

    jrnl @pinkie @WorldDomination

Will print all entries in which either ``@pinkie`` or ``@WorldDomination`` occurred. ::

    jrnl -n 5 -and @pineapple @lubricant

the last five entries containing both ``@pineapple`` **and** ``@lubricant``. You can change which symbols you'd like to use for tagging in the configuration.

.. note::

  ``jrnl @pinkie @WorldDomination`` will switch to viewing mode because although **no** command line arguments are given, all the input strings look like tags - *jrnl* will assume you want to filter by tag.

Editing and deleting entries
----------------------------

Use ``--delete`` to delete entries from your journal. This will only affect selected entries, e.g. ::

    jrnl -n 1 --delete

will delete the last entry, ::

    jrnl @girlfriend -until 'june 2012' --delete

will delete all entries tagged with ``@girlfriend`` written before June 2012. ``jrnl --delete`` would delete your **entire** journal, which is often not what you want. You will be shown the titles of the entries which are about to be deleted before you have to confirm the deletion.

You can also edit selected entries after you wrote them. This is particularly useful when your journal file is encrypted. To use this feature, you need to have an editor configured in your journal configuration file (see :doc:`advanced usage <advanced>`). It behaves the same way ``--delete`` does, ie. ::

    jrnl -until 1950 @texas -and @history --edit

Will edit all entries tagged with ``@texas`` and ``@history`` before 1950. Of course, if you are using multiple journals, you can also edit e.g. the entry of your work journal with ``jrnl work -n 1 --edit``. In any case, this will bring up your editor and save (and, if applicable, encrypt) your edited journal after you save and exit the editor.

