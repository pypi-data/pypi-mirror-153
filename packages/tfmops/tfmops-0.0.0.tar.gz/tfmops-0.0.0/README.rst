========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions| |requires|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/mops/badge/?style=flat
    :target: https://mops.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/tobibias/mops/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/tobibias/mops/actions

.. |requires| image:: https://requires.io/github/tobibias/mops/requirements.svg?branch=main
    :alt: Requirements Status
    :target: https://requires.io/github/tobibias/mops/requirements/?branch=main

.. |version| image:: https://img.shields.io/pypi/v/mops.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/mops

.. |wheel| image:: https://img.shields.io/pypi/wheel/mops.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/mops

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/mops.svg
    :alt: Supported versions
    :target: https://pypi.org/project/mops

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/mops.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/mops

.. |commits-since| image:: https://img.shields.io/github/commits-since/tobibias/mops/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/tobibias/mops/compare/v0.0.0...main



.. end-badges

Morphological Operators implemented with TensorFlow.

* Free software: Apache Software License 2.0

Installation
============

::

    pip install mops

You can also install the in-development version with::

    pip install https://github.com/tobibias/mops/archive/main.zip


Documentation
=============


https://mops.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
