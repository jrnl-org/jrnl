.. _download:

Getting started
===============

Installation
------------

On OS X, the easiest way to install *jrnl* is using `Homebrew <http://brew.sh/>`_

.. code-block:: sh

    brew install jrnl

On other platforms, install *jrnl* using pip

.. code-block:: sh

    pip install jrnl

Or, if you want the option to encrypt your journal,

.. code-block:: sh

    pip install jrnl[encrypted]

to install the dependencies for encrypting journals as well.

.. note::

   Installing the encryption library, `pycryptodome`, requires a `gcc` compiler. For this reason, jrnl will not install `pycryptodome` unless explicitly told so like this. You can install it with ``pip install pycryptodome`` if you have a `gcc` compiler.

   Also note that when using zsh, the correct syntax is ``pip install "jrnl[encrypted]"`` (note the quotes).

The first time you run ``jrnl`` you will be asked where your journal file should be created and whether you wish to encrypt it.


Quickstart
----------

to make a new entry, just type

.. code-block:: sh

    jrnl yesterday: Called in sick. Used the time to clean the house and spent 4h on writing my book.

and hit return. ``yesterday:`` will be interpreted as a time stamp. Everything until the first sentence mark (``.?!:``) will be interpreted as the title, the rest as the body. In your journal file, the result will look like this:

.. code-block:: output

   2012-03-29 09:00 Called in sick.
   Used the time to clean the house and spent 4h on writing my book.

If you just call ``jrnl``, you will be prompted to compose your entry - but you can also configure *jrnl* to use your external editor.

