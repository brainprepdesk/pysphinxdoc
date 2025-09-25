##########################################################################
# pysphinxdoc - Copyright (C) AGrigis, 2025
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

""" Provide usefull functions.
"""

import importlib
import inspect
import pkgutil


def getmembers(module):
    """ Recursively find all the members of a module, and try to apply the
    selection defined in the '__all__' attribute.

    Parameters
    ----------
    mod: ModuleType
        a module.

    Returns
    -------
    members: dict
        structure containing the module names as keys and the associated
        classes and functions names.
    """
    visited, members = set(), {}
    members.update(
        _getmembers(
            module, visited, root_module=module
        )
    )
    if hasattr(module, "__path__"):
        for _finder, name, _ispkg in pkgutil.iter_modules(module.__path__):
            try:
                submodule_name = f"{module.__name__}.{name}"
                submodule = importlib.import_module(submodule_name)
            except Exception as e:
                print(f"Could not import submodule '{submodule_name}': {e}")
            members.update(
                _getmembers(
                    submodule, visited, root_module=submodule
                )
            )
    to_drop = set()
    for key, data in members.items():
        if len(data["functions"]) == 0 and len(data["classes"]) == 0:
            to_drop.add(key)
    for key in to_drop:
        del members[key]
    return members


def _getmembers(module, visited, root_module=None):
    """ Return the members of a module, and try to apply the selection
    defined in the '__all__' attribute.

    Parameters
    ----------
    mod: ModuleType
        a module.
    visited: set
        a list of already visited modules.
    root_module: ModuleType, default None
        the root module used to not go too deep.

    Returns
    -------
    members: dict
        structure containing the module names as keys and the asssociated
        classes and functions names.
    """
    module_name = module.__name__
    if module_name in visited:
        return {}
    visited.add(module_name)
    members = {}
    root_module = root_module or module

    members[module_name] = {"functions": [], "classes": []}

    selection = module.__all__ if hasattr(module, "__all__") else dir(module)
    for name, member in inspect.getmembers(module):
        if inspect.ismodule(member):
            if member.__name__.startswith(root_module.__name__):
                members.update(
                    _getmembers(
                        member, visited, root_module=root_module
                    )
                )
        elif inspect.isfunction(member):
            if name in selection and member.__module__.startswith(module_name):
                members[module_name]["functions"].append(
                    name
                )
        elif inspect.isclass(member):
            if name in selection and member.__module__.startswith(module_name):
                members[module_name]["classes"].append(
                    name
                )
    return members
