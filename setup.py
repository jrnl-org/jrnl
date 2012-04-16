from setuptools import setup, find_packages
import os.path
import sys

install_requires = ["parsedatetime", "pycrypto", "hashlib"]
if sys.version_info < (2, 6):
    install_requires.append("simplejson")

base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name = "jrnl",
    version = "0.2.0",
    description = "A command line journal application that stores your journal in a plain text file",

    packages = find_packages(),
    scripts = ['jrnl.py'],
    install_requires = install_requires,

    long_description="\n".join([
        open(os.path.join(base_dir, "README.md"), "r").read(),
        open(os.path.join(base_dir, "CHANGELOG.md"), "r").read()
    ]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: Freely Distributable',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business :: News/Diary',
        'Topic :: Text Processing'
    ],
    # metadata for upload to PyPI
    author = "Manuel Ebert",
    author_email = "manuel.ebert@upf.edu",
    license = "MIT License",
    keywords = "journal todo todo.txt jrnl".split(),
    url = "http://maebert.github.com/jrnl",   # project home page, if any
)