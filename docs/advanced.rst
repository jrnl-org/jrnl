.. _advanced:

Advanced Usage
==============

Configuration File
-------------------

You can configure the way jrnl behaves in a configuration file. By default, this is ``~/.jrnl_config``. If you have the ``XDG_CONFIG_HOME`` variable set, the configuration file will be saved under ``$XDG_CONFIG_HOME/jrnl``.

.. note::

    On Windows, The configuration file is typically found at ``C:\Users\[Your Username]\.jrnl_config``.


The configuration file is a simple JSON file with the following options and can be edited with any plain text editor.

- ``journals``
      paths to your journal files
- ``editor``
    if set, executes this command to launch an external editor for writing your entries, e.g. ``vim``. Some editors require special options to work properly, see :doc:`FAQ <recipes>` for details.
- ``encrypt``
    if ``true``, encrypts your journal using AES.
- ``tagsymbols``
    Symbols to be interpreted as tags. (See note below)
- ``default_hour`` and ``default_minute``
    if you supply a date, such as ``last thursday``, but no specific time, the entry will be created at this time
- ``timeformat``
    how to format the timestamps in your journal, see the `python docs <http://docs.python.org/library/time.html#time.strftime>`_ for reference
- ``highlight``
    if ``true``, tags will be highlighted in cyan.
- ``linewrap``
    controls the width of the output. Set to ``false`` if you don't want to wrap long lines.

.. note::

      Although it seems intuitive to use the `#` character for tags, there's a drawback: on most shells, this is interpreted as a meta-character starting a comment. This means that if you type

      .. code-block:: note

          jrnl Implemented endless scrolling on the #frontend of our website.

      your bash will chop off everything after the ``#`` before passing it to _jrnl_). To avoid this, wrap your input into quotation marks like this:

      .. code-block:: note

          jrnl "Implemented endless scrolling on the #frontend of our website."

      Or use the built-in prompt or an external editor to compose your entries.

DayOne Integration
------------------

Using your DayOne journal instead of a flat text file is dead simple -- instead of pointing to a text file, change your ``.jrnl_config`` to point to your DayOne journal. This is a folder named something like ``Journal_dayone`` or ``Journal.dayone``, and it's located at

* ``~/Library/Application Support/Day One/`` by default
* ``~/Dropbox/Apps/Day One/`` if you're syncing with Dropbox and
* ``~/Library/Mobile Documents/5U8NS4GX82~com~dayoneapp~dayone/Documents/`` if you're syncing with iCloud.

Instead of all entries being in a single file, each entry will live in a separate `plist` file. So your ``.jrnl_config`` should look like this:

.. code-block:: javascript

    {
      ...
      "journals": {
        "default": "~/journal.txt",
        "dayone": "~/Library/Mobile Documents/5U8NS4GX82~com~dayoneapp~dayone/Documents/Journal_dayone"
    }


Alfred Integration
------------------

You can use _jrnl_ with the popular `Alfred <https://www.alfredapp.com/>`_ app with `this handy workflow <http://www.packal.org/workflow/jrnl>`_.


Multiple journal files
----------------------

You can configure _jrnl_ to use with multiple journals (eg. ``private`` and ``work``) by defining more journals in your ``.jrnl_config``, for example:

.. code-block:: javascript

    {
    ...
      "journals": {
        "default": "~/journal.txt",
        "work":    "~/work.txt"
      }
    }

The ``default`` journal gets created the first time you start _jrnl_. Now you can access the ``work`` journal by using ``jrnl work`` instead of ``jrnl``, eg. ::

    jrnl work at 10am: Meeting with @Steve

::

    jrnl work -n 3

will both use ``~/work.txt``, while ``jrnl -n 3`` will display the last three entries from ``~/journal.txt`` (and so does ``jrnl default -n 3``).

You can also override the default options for each individual journal. If you ``.jrnl_config`` looks like this:

.. code-block:: javascript

    {
      ...
      "encrypt": false
      "journals": {
        "default": "~/journal.txt",
        "work": {
          "journal": "~/work.txt",
          "encrypt": true
        },
        "food": "~/my_recipes.txt",
    }

Your ``default`` and your ``food`` journals won't be encrypted, however your ``work`` journal will! You can override all options that are present at the top level of ``.jrnl_config``, just make sure that at the very least you specify a ``"journal": ...`` key that points to the journal file of that journal.

.. note::

    Changing ``encrypt`` to a different value will not encrypt or decrypt your journal file, it merely says whether or not your journal `is` encrypted. Hence manually changing this option will most likely result in your journal file being impossible to load.

Known Issues
~~~~~~~~~~~~

- The Windows shell prior to Windows 7 has issues with Unicode encoding. If you want to use non-ASCII characters, change the code page with ``chcp 1252`` before using `jrnl` (Thanks to Yves Pouplard for solving this!)
- _jrnl_ relies on the `PyCrypto` package to encrypt journals, which has some known problems with installing on Windows and within virtual environments.
