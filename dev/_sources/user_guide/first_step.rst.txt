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
