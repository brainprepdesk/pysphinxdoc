##########################################################################
# pysphinxdoc - Copyright (C) AGrigis, 2025
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

""" Provide a command line interface.
"""


def generate_documentation(
        path_module,
        name_module,
        mock=None,
        mock_params=None,
        mock_returns=None,
        verbose=0):
    """ Script to prepare you Sphinx documentation.

    Parameters
    ----------
    path_module: str
        the path to the module to be documented.
    name_module: str
        the name of the module to be documented.
    mock: list, default None
        mock some modules if dependencies cannot be installed when building
        the project.
    mock_params: list, default None
        the parameters returned by mocked modules.
    mock_returns: listy, default None
        the parameters values returned by mocked modules.
    verbose: int, default 0
        control the verbosity level.
    """
    import sys
    from unittest.mock import MagicMock

    import pysphinxdoc
    from pysphinxdoc.docgen import DocWriter

    # Mock uninstalled modules
    mock_kwargs = {}
    if mock_params is not None:
        for key, val_repr in zip(mock_params, mock_returns, strict=True):
            mock_kwargs[key] = eval(val_repr)

    class Mock(MagicMock):
        @classmethod
        def __getattr__(cls, name):
            return MagicMock(**mock_kwargs)

    if mock is not None:
        sys.modules.update((mod_name, Mock()) for mod_name in mock)

    # Get all the modules involved
    if verbose > 0:
        print(f"[info] Using pysphinxdoc {pysphinxdoc.__version__}")
        print(f"[info] Documenting {name_module} ...")

    # Generate a sphinx layout, API documentation, and Sphinx configuration.
    docwriter = DocWriter(
        path_module,
        name_module,
        verbose=verbose
    )
    docwriter.write_layout()
    docwriter.write_api_search()
    docwriter.write_api_doc()

    if verbose > 0:
        print("[info] Done.")


def generate_documentation_main():
    import fire

    fire.Fire(generate_documentation)
