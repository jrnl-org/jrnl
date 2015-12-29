.. _download:

Getting started
===============

Installation
------------

Install *jrnl* using pip ::

    pip install jrnl

Alternatively, on OS X with [Homebrew](http://brew.sh/) installed:

    brew install jrnl

The first time you run ``jrnl`` you will be asked where your journal file should be created and whether you wish to encrypt it.


Quickstart
----------

to make a new entry, just type::

    jrnl yesterday: Called in sick. Used the time to clean the house and spent 4h on writing my book.

and hit return. ``yesterday:`` will be interpreted as a time stamp. Everything until the first sentence mark (``.?!:``) will be interpreted as the title, the rest as the body. In your journal file, the result will look like this:

.. code-block:: output

   2012-03-29 09:00 Called in sick.
   Used the time to clean the house and spent 4h on writing my book.

If you just call ``jrnl``, you will be prompted to compose your entry - but you can also configure *jrnl* to use your external editor.

