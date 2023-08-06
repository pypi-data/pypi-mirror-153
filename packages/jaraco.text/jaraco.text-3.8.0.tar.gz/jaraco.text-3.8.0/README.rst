.. image:: https://img.shields.io/pypi/v/jaraco.text.svg
   :target: `PyPI link`_

.. image:: https://img.shields.io/pypi/pyversions/jaraco.text.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/jaraco.text

.. image:: https://github.com/jaraco/jaraco.text/workflows/tests/badge.svg
   :target: https://github.com/jaraco/jaraco.text/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. image:: https://readthedocs.org/projects/jaracotext/badge/?version=latest
   :target: https://jaracotext.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2022-informational
   :target: https://blog.jaraco.com/skeleton


Layouts
=======

One of the features of this package is the layouts module, which
provides a simple example of translating keystrokes from one keyboard
layout to another::

    echo qwerty | python -m jaraco.text.to-dvorak
    ',.pyf
    echo  "',.pyf" | python -m jaraco.text.to-qwerty
    qwerty
