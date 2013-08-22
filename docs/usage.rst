.. _usage:

Basic Usage
===========

*jrnl* has two modes: **composing** and **viewing**.

Viewing
-------

::

    jrnl -n 10

will list you the ten latest entries, ::

    jrnl -from "last year" -to march

everything that happened from the start of last year to the start of last march. If you only want to see the titles of your entries, use ::

    jrnl -short

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

  ``jrnl @pinkie @WorldDomination`` will switch to viewing mode because although _no_ command line arguments are given, all the input strings look like tags - *jrnl* will assume you want to filter by tag.


Composing
---------

Composing mode is entered by either starting ``jrnl`` without any arguments -- which will prompt you to write an entry or launch your editor -- or by just writing an entry on the prompt, such as::

    jrnl today at 3am: I just met Steve Buscemi in a bar! He looked funny.


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
