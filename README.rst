**Usage**

.. image:: https://img.shields.io/badge/python-3.12-blue
    :target: https://github.com/AGrigis/pysphinxdoc
    :alt: Python Version

.. image:: https://img.shields.io/badge/License-CeCILL--B-blue.svg
    :target: http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
    :alt: License

**Development**

.. image:: https://github.com/AGrigis/pysphinxdoc/actions/workflows/pep8.yml/badge.svg
    :target: https://github.com/AGrigis/pysphinxdoc/actions
    :alt: Github Actions Linter Status

.. image:: https://github.com/AGrigis/pysphinxdoc/actions/workflows/documentation.yml/badge.svg
    :target: http://AGrigis.github.io/pysphinxdoc
    :alt: Github Actions Doc Build Status

**Release**

.. image:: https://badge.fury.io/py/pysphinxdoc.svg
    :target: https://badge.fury.io/py/pysphinxdoc
    :alt: Pypi Package


pysphinxdoc
===========

Pysphinxdoc is a tool for generating automatically API documentation
for Python modules, based on their reStructuredText docstrings, using
`Sphinx <http://www.sphinx-doc.org/>`_.


Important links
===============

- Official source code repo: https://github.com/AGrigis/pysphinxdoc
- HTML documentation (stable release): https://AGrigis.github.io/pysphinxdoc/stable
- HTML documentation (dev): https://AGrigis.github.io/pysphinxdoc/dev


Install
=======

Latest release
--------------

**1. Setup a virtual environment**

We recommend that you install ``pysphinxdoc`` in a virtual Python environment,
either managed with the standard library ``venv`` or with ``conda``.
Either way, create and activate a new python environment.

With ``venv``:

.. code-block:: bash

    python3 -m venv /<path_to_new_env>
    source /<path_to_new_env>/bin/activate

Windows users should change the last line to ``\<path_to_new_env>\Scripts\activate.bat``
in order to activate their virtual environment.

With ``conda``:

.. code-block:: bash

    conda create -n pysphinxdoc python=3.12
    conda activate pysphinxdoc

**2. Install pysphinxdoc with pip**

Execute the following command in the command prompt / terminal
in the proper python environment:

.. code-block:: bash

    python3 -m pip install -U pysphinxdoc


Check installation
------------------

Try importing pysphinxdoc in a python / iPython session:

.. code-block:: python

    import pysphinxdoc

If no error is raised, you have installed pysphinxdoc correctly.


Dependencies
============

The required dependencies to use the software are listed
in the file `pyproject.toml <https://github.com/AGrigis/pysphinxdoc/blob/main/pyproject.toml>`_.
