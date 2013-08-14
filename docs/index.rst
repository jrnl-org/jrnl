.. jrnl documentation master file, created by
   sphinx-quickstart on Wed Aug  7 13:22:51 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

jrnl: The command-line journal
==============================

Release v\ |version|. (:ref:`Installation <install>`)


    >>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
    >>> r.status_code
    200
    >>> r.headers['content-type']
    'application/json; charset=utf8'
    >>> r.encoding
    'utf-8'
    >>> r.text
    u'{"type":"User"...'
    >>> r.json()
    {u'private_gists': 419, u'total_private_repos': 77, ...}

.. autofunction:: jrnl
.. autofunction:: jrnl.Journal


Contents:

.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

