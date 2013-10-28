#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jrnl is a simple journal application for your command line. Journals are stored as human readable plain text files - you can put them into a Dropbox folder for instant syncinc and you can be assured that your journal will still be readable in 2050, when all your fancy iPad journal applications will long be forgotten.

Optionally, your journal can be encrypted using 256-bit AES.

Why keep a journal?
```````````````````

Journals aren't only for 13-year old girls and people who have too much time on their summer vacation. A journal helps you to keep track of the things you get done and how you did them. Your imagination may be limitless, but your memory isn't. For personal use, make it a good habit to write at least 20 words a day. Just to reflect what made this day special, why you haven't wasted it. For professional use, consider a text-based journal to be the perfect complement to your GTD todo list - a documentation of what and how you've done it.

In a Nutshell
`````````````

to make a new entry, just type

::

    jrnl yesterday: Called in sick. Used the time to clean the house and spent 4h on writing my book.

and hit return. yesterday` will be interpreted as a timestamp. Everything until the first sentence mark (.?!) will be interpreted as the title, the rest as the body. In your journal file, the result will look like this:

::

    2012-03-29 09:00 Called in sick.
    Used the time to clean the house and spent 4h on writing my book.

If you just call jrnl you will be prompted to compose your entry - but you can also configure jrnl to use your external editor.

Links
`````

* `website & documentation <http://maebert.github.com/jrnl>`_
* `GitHub Repo <https://github.com/maebert/jrnl>`_

"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os
import sys
import re

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    sys.exit()

base_dir = os.path.dirname(os.path.abspath(__file__))

def get_version(filename="jrnl/__init__.py"):
    with open(os.path.join(base_dir, filename)) as initfile:
        for line in initfile.readlines():
            m = re.match("__version__ *= *['\"](.*)['\"]", line)
            if m:
                return m.group(1)

conditional_dependencies = {
    "pyreadline>=2.0": "win32" in sys.platform,
    "argparse==1.2.1": sys.version.startswith("2.6")
}

setup(
    name = "jrnl",
    version = get_version(),
    description = "A command line journal application that stores your journal in a plain text file",
    packages = ['jrnl'],
    install_requires = [
        "parsedatetime>=1.1.2",
        "pytz>=2013b",
        "tzlocal==1.0",
        "slugify>=0.0.1",
        "colorama>=0.2.5",
        "keyring>=3.0.5"
        ] + [p for p, cond in conditional_dependencies.items() if cond],
    extras_require = {
        "encrypted": "pycrypto>=2.6"
    },
    long_description=__doc__,
    entry_points={
        'console_scripts': [
            'jrnl = jrnl:cli',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Office/Business :: News/Diary',
        'Topic :: Text Processing'
    ],
    # metadata for upload to PyPI
    author = "Manuel Ebert",
    author_email = "manuel@1450.me",
    license = "MIT License",
    keywords = "journal todo todo.txt jrnl".split(),
    url = "http://maebert.github.io/jrnl",
)
