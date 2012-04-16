from setuptools import setup, find_packages
import os.path
import sys

install_requires = ["parsedatetime", "pycrypto"]
if sys.version_info < (2, 6):
    install_requires.append("simplejson")

base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name = "jrnl",
    version = "0.1.1",
    description = "A command line journal application that stores your journal in a plain text file",

    packages = find_packages(),
    scripts = ['jrnl.py'],
    install_requires = install_requires,

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    long_description="\n\n".join([
        open(os.path.join(base_dir, "README.md"), "r").read(),
        open(os.path.join(base_dir, "CHANGELOG.md"), "r").read()
    ]),

    # metadata for upload to PyPI
    author = "Manuel Ebert",
    author_email = "manuel.ebert@upf.edu",
    license = "MIT",
    keywords = "journal todo todo.txt jrnl".split(),
    url = "http://maebert.github.com/jrnl",   # project home page, if any
)