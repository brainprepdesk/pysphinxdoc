First step with ``pysphinxdoc``
===============================


Import resources
----------------

The module comes with a script that can be used to generate all the resources
required to generate your documentation withing your ``doc`` folder.
Let's consider the GIT_PATH variable, that contains the path to your git
cloned repositories and that you want to document the ``pysphinxdoc``
module.

.. code-block:: bash

    sphinxdoc -v 2 -p $GIT_PATH/pysphinxdoc -n pysphinxdoc

The documentation is generated from the reStructuredText docstrings of each
module, function or class.

Note that with ``__all__`` defined, the module will only document the names
listed in ``__all__``. Without ``__all__`` defined, the module will document
all public names (those not starting with _).

.. hint::

    This means ``__all__`` acts as a gatekeeper for what gets included in
    your generated docs — just like it does for ``from module import *``.

.. note::

    In Python, ``__all__`` is a special variable used in modules to define
    what symbols (functions, classes, variables, etc.) should be exported
    when ``from module import *`` is used:

    - it controls the public API of a module.
    - it helps hide internal details and expose only what's meant to be used
      externally.

    The ``__all__`` variable is defined as a list of strings at the top level
    of a module.


Complile documentation
----------------------

Then you can simply compile your documentation with Sphinx

.. code-block:: bash

    cd $GIT_PATH/pysphinxdoc/pysphinxdoc/doc
    make html


Options
-------

Different compilation options have been made available.


============ =================================================================================
Options
============ =================================================================================
html         Default build.

html-strict  Build html documentation using a strict mode: Warnings are considered as errors.

html-noplot  Build html documentation without running examples.
============ =================================================================================
