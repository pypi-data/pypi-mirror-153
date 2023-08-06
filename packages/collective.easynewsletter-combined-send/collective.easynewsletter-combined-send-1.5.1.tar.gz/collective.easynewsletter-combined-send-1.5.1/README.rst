.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://coveralls.io/repos/github/collective/collective.easynewsletter-combined-send/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.easynewsletter-combined-send?branch=master
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/collective.easynewsletter-combined-send.svg
    :target: https://pypi.python.org/pypi/collective.easynewsletter-combined-send/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/collective.easynewsletter-combined-send.svg?style=plastic
    :alt: Supported - Python Versions



=======================================
collective.easynewsletter-combined-send
=======================================

Extend EasyNewsletter to send languages combined one email on top of each other.
For now it only works well for one lange plus english version as alternative below.
Because the text of the link is hard wired in the issuedatafetcher.


Features
--------

- If you sent a newsletter issue and have translated it into other languages, the issues will get the content of all translation and combined them in one newsletter issue.


Installation
------------

Install collective.easynewsletter-combined-send by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.easynewsletter-combined-send


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.easynewsletter-combined-send/issues
- Source Code: https://github.com/collective/collective.easynewsletter-combined-send


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the GPLv2.
