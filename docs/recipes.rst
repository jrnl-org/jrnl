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

Statistics
~~~~~~~~~~

How much did I write last year? ::

    jrnl -from "jan 1 2013" -until "dec 31 2013" | wc -w

Will give you the number of words you wrote in 2013. How long is my average entry? ::

    expr $(jrnl --export text | wc -w) / $(jrnl --short | wc -l)

This will first get the total number of words in the journal and divide it by the number of entries (this works because ``jrnl --short`` will print exactly one line per entry).

Importing older files
~~~~~~~~~~~~~~~~~~~~~

If you want to import a file as an entry to jrnl, you can just do ``jrnl < entry.ext``. But what if you want the modification date of the file to be the date of the entry in jrnl? Try this ::

    echo `stat -f %Sm -t '%d %b %Y at %H:%M: ' entry.txt` `cat entry.txt` | jrnl

The first part will format the modification date of ``entry.txt``, and then combine it with the contents of the file before piping it to jrnl. If you do that often, consider creating a function in your ``.bashrc`` or ``.bash_profile``

.. code-block:: sh

    jrnlimport () {
        echo `stat -f %Sm -t '%d %b %Y at %H:%M: ' $1` `cat $1` | jrnl
    }


Using templates
~~~~~~~~~~~~~~~

Say you always want to use the same template for creating new entries. If you have an :doc:`external editor <advanced>` set up, you can use this ::

    jrnl < my_template.txt
    $ jrnl -1 --edit

Another nice solution that allows you to define individual prompts comes from `Jacobo de Vera <https://github.com/maebert/jrnl/issues/194#issuecomment-47402869>`_:

.. code-block:: sh

    function log_question()
    {
       echo $1
       read
       jrnl today: ${1}. $REPLY
    }
    log_question 'What did I achieve today?'
    log_question 'What did I make progress with?'


External editors
----------------

To use external editors for writing and editing journal entries,  set them up in your ``.jrnl_config`` (see :doc:`advanced usage <advanced>` for details). Generally, after writing an entry, you will have to save and close the file to save the changes to jrnl.

Sublime Text
~~~~~~~~~~~~

To use Sublime Text, install the command line tools for Sublime Text and configure your ``.jrnl_config`` like this:

.. code-block:: javascript

    "editor": "subl -w"

Note the ``-w`` flag to make sure jrnl waits for Sublime Text to close the file before writing into the journal.


MacVim
~~~~~~

Similar to Sublime Text, MacVim must be started with a flag that tells the the process to wait until the file is closed before passing control back to journal. In the case of MacVim, this is ``-f``:

.. code-block:: javascript

    "editor": "mvim -f"

iA Writer
~~~~~~~~~

On OS X, you can use the fabulous `iA Writer <http://www.iawriter.com/mac>`_ to write entries. Configure your ``.jrnl_config`` like this:

.. code-block:: javascript

    "editor": "open -b jp.informationarchitects.WriterForMacOSX -Wn"

What does this do? ``open -b ...`` opens a file using the application identified by the bundle identifier (a unique string for every app out there). ``-Wn`` tells the application to wait until it's closed before passing back control, and to use a new instance of the application.


Notepad++ on Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To set `Notepad++ <http://notepad-plus-plus.org/>`_ as your editor, edit the jrnl config file (``.jrnl_config``) like this:

.. code-block:: javascript

      "editor": "C:\\Program Files (x86)\\Notepad++\\notepad++.exe -multiInst -nosession",

The double backslashes are needed so jrnl can read the file path correctly. The ``-multiInst -nosession`` options will cause jrnl to open its own Notepad++ window.

Visual Studio Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To set `Visual Studo Code <https://code.visualstudio.com/>`_ as your editor on Linux, edit ``.jrnl_config`` like this: 

.. code-block:: javascript

	"editor": "/usr/bin/code --wait",

The --wait argument tells VS Code to wait for files to be written out before handing back control to jrnl.

On MacOS you will need to add VS Code to your PATH. You can do that by adding:

.. code-block:: bash

	export PATH="\$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"

to your .bash_profile, or by running the **Install 'code' command in PATH** command from the command pallet in VS Code.

Then you can add:

.. code-block:: javascript
	
	"editor": "code --wait",
	
to ``.jrnl_config``. See also `the Visual Studio Code documentation <https://code.visualstudio.com/docs/setup/mac>`_.
