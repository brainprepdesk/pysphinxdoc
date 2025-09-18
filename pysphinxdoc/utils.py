##########################################################################
# pysphinxdoc - Copyright (C) AGrigis, 2025
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

""" Provide usefull functions.
"""

import inspect


def getmembers(module, root_module=None):
    """ Return the members of a module, and try to apply the selection
    defined in the '__all__' attribute.

    Parameters
    ----------
    mod: ModuleType
        a module.
    root_module: ModuleType
        the root module used to not go too deep.

    Returns
    -------
    members: dict
        structure containing the module names as keys and the asssociated
        classes and functions names.
    """
    members = {}
    root_module = root_module or module
    module_name = module.__name__
    members[module_name] = {"functions": [], "classes": []}
    selection = module.__all__ if hasattr(module, "__all__") else []
    for name, member in inspect.getmembers(module):
        if inspect.ismodule(member):
            if member.__name__.startswith(root_module.__name__):
                members.update(
                    getmembers(member, root_module)
                )
        elif inspect.isfunction(member):
            if name in selection or member.__module__.startswith(module_name):
                members[module_name]["functions"].append(
                    f"{module_name}.{name}"
                )
        elif inspect.isclass(member):
            if name in selection or member.__module__.startswith(module_name):
                members[module_name]["classes"].append(
                    f"{module_name}.{name}"
                )
    return members
