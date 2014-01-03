.. _recipes:

FAQ
===

Recipes
-------

Co-occurrence of tags
~~~~~~~~~~~~~~~~~~~~~

If I want to find out how often I mentioned my flatmates Alberto and Melo in the same entry, I run ::

    jrnl @alberto --tags | grep @melo

And will get something like ``@melo: 9``, meaning there are 9 entries where both ``@alberto`` and ``@melo`` are tagged. How does this work? First, ``jrnl @alberto`` will filter the journal to only entries containing the tag ``@alberto``, and then the ``--tags`` option will print out how often each tag occurred in this `filtered` journal. Finally, we pipe this to ``grep`` which will only display the line containing ``@melo``.

Combining filters
~~~~~~~~~~~~~~~~~

You can do things like ::

    jrnl @fixed -starred -n 10 -until "jan 2013" --short

To get a short summary of the 10 most recent, favourited entries before January 1, 2013 that are tagged with ``@fixed``.


Using iA Writer to write entries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On OS X, you can use the fabulous `iA Writer <http://www.iawriter.com/mac>`_ to write entries. Configure your ``.jrnl_conf`` like this:

.. code-block:: javascript

    "editor": "open -b jp.informationarchitects.WriterForMacOSX -Wn"

What does this do? ``open -b ...`` opens a file using the application identified by the bundle identifier (a unique string for every app out there). ``-Wn`` tells the application to wait until it's closed before passing back control, and to use a new instance of the application.


Using Notepad++ to write entries on Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    The configuration file is typically found at ``C:\Users\[Your Username]\.jrnl_conf``. This is just a text file and so can be edited in a text editor (but don't use Notepad, it will mess with the line endings).

To set `Notepad++ <http://notepad-plus-plus.org/>`_ as your editor, edit the jrnl config file (``.jrnl_conf``) like this:

.. code-block:: javascript

    {
      ...
      "editor": "C:\\Program Files (x86)\\Notepad++\\notepad++.exe -multiInst",
    }

The double backslashes are needed so jrnl can read the file path correctly. The ``-multiInst`` option will cause jrnl to open its own Notepad++ window. When you're done editing an entry in Notepad++, save the file and close the Notepad++ window for jrnl to know you're done editing and record your changes.


Known Issues
------------

- The Windows shell prior to Windows 7 has issues with unicode encoding. If you want to use non-ascii characters, change the codepage with ``chcp 1252`` before using `jrnl` (Thanks to Yves Pouplard for solving this!)
- _jrnl_ relies on the `PyCrypto` package to encrypt journals, which has some known problems with installing on Windows and within virtual environments.
