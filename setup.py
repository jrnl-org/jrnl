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
try:
    import readline
    readline_available = True
except ImportError:
    readline_available = False


base_dir = os.path.dirname(os.path.abspath(__file__))

def get_version(filename="jrnl/__init__.py"):
    with open(os.path.join(base_dir, filename)) as initfile:
        for line in initfile.readlines():
            m = re.match("__version__ *= *['\"](.*)['\"]", line)
            if m:
                return m.group(1)


def get_changelog(filename="CHANGELOG.md"):
    changelog = {}
    current_version = None
    with open(os.path.join(base_dir, filename)) as changelog_file:
        for line in changelog_file.readlines():
            if line.startswith("* __"):
                parts = line.strip("* ").split(" ", 1)
                if len(parts) == 2:
                    current_version, changes = parts[0].strip("_\n"), parts[1]
                    changelog[current_version] = [changes.strip()]
                else:
                    current_version = parts[0].strip("_\n")
                    changelog[current_version] = []
            elif line.strip() and current_version and not line.startswith("#"):
                changelog[current_version].append(line.strip(" *\n"))
    return changelog

def dist_pypi():
    os.system("python setup.py sdist upload")
    sys.exit()

def dist_github():
    """Creates a release on the maebert/jrnl repository on github"""
    import requests
    import keyring
    import getpass
    version = get_version()
    version_tuple = version.split(".")
    changes_since_last_version = ["* __{}__: {}".format(key, "\n".join(changes)) for key, changes in get_changelog().items() if key.startswith("{}.{}".format(*version_tuple))]
    changes_since_last_version = "\n".join(sorted(changes_since_last_version, reverse=True))
    payload = {
        "tag_name": version,
        "target_commitish": "master",
        "name": version,
        "body": "Changes in Version {}.{}: \n\n{}".format(version_tuple[0], version_tuple[1], changes_since_last_version)
    }
    print("Preparing release {}...".format(version))
    username = keyring.get_password("github", "__default_user") or raw_input("Github username: ")
    password = keyring.get_password("github", username) or getpass.getpass()
    otp = raw_input("One Time Token: ")
    response = requests.post("https://api.github.com/repos/maebert/jrnl/releases", headers={"X-GitHub-OTP": otp}, json=payload, auth=(username, password))
    if response.status_code in (403, 404):
        print("Authentication error.")
    else:
        keyring.set_password("github", "__default_user", username)
        keyring.set_password("github", username, password)
        if response.status_code > 299:
            if  "message" in response.json():
                print("Error: {}".format(response.json()['message']))
                for error_dict in response.json().get('errors', []):
                    print("*", error_dict)
            else:
                print("Unkown error")
                print(response.text)
        else:
            print("Release created.")
    sys.exit()

if sys.argv[-1] == 'publish':
    dist_pypi()

if sys.argv[-1] == 'github_release':
    dist_github()

conditional_dependencies = {
    "pyreadline>=2.0": not readline_available and "win32" in sys.platform,
    "readline>=6.2": not readline_available and "win32" not in sys.platform,
    "colorama>=0.2.5": "win32" in sys.platform,
    "argparse>=1.1.0": sys.version.startswith("2.6"),
    "python-dateutil==1.5": sys.version.startswith("2."),
    "python-dateutil>=2.2": sys.version.startswith("3."),
}


setup(
    name = "jrnl",
    version = get_version(),
    description = "A command line journal application that stores your journal in a plain text file",
    packages = ['jrnl'],
    install_requires = [
        "parsedatetime>=1.2",
        "pytz>=2013b",
        "six>=1.6.1",
        "tzlocal>=1.1",
        "keyring>=3.3",
    ] + [p for p, cond in conditional_dependencies.items() if cond],
    extras_require = {
        "encrypted": "pycrypto>=2.6"
    },
    long_description=__doc__,
    entry_points={
        "console_scripts": [
            "jrnl = jrnl:run",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Text Processing"
    ],
    # metadata for upload to PyPI
    author = "Manuel Ebert",
    author_email = "manuel@1450.me",
    license="LICENSE",
    keywords = "journal todo todo.txt jrnl".split(),
    url = "http://www.jrnl.sh",
)
