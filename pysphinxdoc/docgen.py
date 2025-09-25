##########################################################################
# pysphinxdoc - Copyright (C) AGrigis, 2016 - 2025
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

""" Provide a 'DocHelperWriter' class to generate a Sphinx complient
documentation of a module.
"""

import glob
import importlib
import os
import shutil
import sys
import textwrap
from pprint import pprint

from distutils.dir_util import copy_tree

from .utils import getmembers


class DocWriter:
    """ A basic class to create a Sphinx complient documentation of a module.

    Parameters
    ----------
    module_dir: str
        the path to the module to be documented. This must contain a
        'doc' folder where the documentation will be generated, organized
        as follows:

        - logos: '$name.png', '$name-transparent.png',
          '$name-desaturate-100.png'
        - user_guide (optional): 'index.rst', '.rst'
    module_name: list of str
        the name of the python package to be documented.
    verbose: int, default 0
        the verbosity level.

    Notes
    -----
    Prefer to use directly the ``sphinxdoc`` script.
    """
    def __init__(
            self,
            module_dir,
            module_name,
            verbose=0):
        """ Initialize the class.
        """
        # Load the module to be documented
        importlib.import_module(module_name)
        self.module = sys.modules[module_name]

        # Generate destination folders
        self.outdir = os.path.join(module_dir, "doc")
        self.logodir = os.path.join(self.outdir, "logos")
        self.guidedir = os.path.join(self.outdir, "user_guide")
        self.apidir = os.path.join(self.outdir, "modules")
        for path in (self.outdir, self.logodir):
            if not os.path.isdir(path):
                raise NotADirectoryError(path)
        if not os.path.isdir(self.guidedir):
            self.guidedir = None
        if os.path.isdir(self.apidir):
            raise OSError(
                f"'{self.apidir}' already created, can't delete it "
                "automatically. Use the Makefile to generate the "
                "documentation using the 'make html', 'make html-strict', "
                "'make html-modified-examples-only', or 'make html-noplot' "
                "commands."
            )
        os.mkdir(self.apidir)

        # Instance parameters
        self.moduledir = module_dir
        self.module_name = module_name
        self.verbose = verbose
        self.resourcedir = os.path.join(
            os.path.dirname(__file__),
            "resources"
        )

        # Get module members
        self.module_members = getmembers(self.module)
        if self.verbose > 1:
            pprint(self.module_members)

    def write_layout(self):
        """ Generate the Sphinx layout.
        """
        if self.verbose > 0:
            print("[info] Generating layout...")
        copy_tree(self.resourcedir, self.outdir)
        conf_file = os.path.join(self.outdir, "conf.py")
        index_file = os.path.join(self.outdir, "index.jinja")
        default_files = glob.glob(
            os.path.join(self.outdir, "default", "*")
        )
        project_title = self.module_name
        project_title += f"\n{'=' * len(project_title)}"
        info = {
            "project": self.module_name,
            "project_title": project_title,
            "user_guide": (
                "user_guide/index.rst" if self.guidedir is not None else ""
            ),
            "description": textwrap.dedent(
                self.module.__doc__ or ""
            )
        }
        for path in [*default_files, conf_file, index_file]:
            self.write_from_template(path, info, verbose=self.verbose)

    def write_api_search(self):
        """ Generate the API search page.
        """
        if self.verbose > 0:
            print("[info] Generating API search page...")
        template_file = os.path.join(
            self.resourcedir, "templates", "search.rst"
        )
        search_file = os.path.join(self.apidir, "search.rst")
        shutil.copy(template_file, search_file)
        entries = []
        for mod, members in self.module_members.items():
            for otype in ("classes", "functions"):
                entries.extend(
                    [f"{mod}.{obj}" for obj in members[otype]]
                )
        entries = [
            f"<li><a href='generated/{name}.html'>{name}</a></li>"
            for name in sorted(entries)
        ]
        info = {
            "project": self.module_name,
            "entries": textwrap.indent(
                "\n".join(entries), "      ", lambda line: True
            )
        }
        self.write_from_template(search_file, info, verbose=self.verbose)

    def write_api_doc(self):
        """ Generate the API documentation.
        """
        # Welcome message
        if self.verbose > 0:
            print("[info] Generating API documentation...")

        # Generate reST API of each module
        if self.verbose > 1:
            print(f"[debug] processing {self.module_name}...")

        # Write module API doc to file
        index = []
        class_template_file = os.path.join(
            self.resourcedir, "templates", "modules_class.rst"
        )
        function_template_file = os.path.join(
            self.resourcedir, "templates", "modules_function.rst"
        )
        for module_name, data in self.module_members.items():
            functions, klasses = data["functions"], data["classes"]
            if len(functions) == 0 and len(klasses) == 0:
                continue
            template_file = os.path.join(
                self.resourcedir, "templates", "modules.rst"
            )
            outfile = os.path.join(self.apidir, f"{module_name}.rst")
            shutil.copy(template_file, outfile)
            index.append(os.path.basename(outfile))
            importlib.import_module(module_name)
            module = sys.modules[module_name]
            classes_description = self.edit_from_template(
                class_template_file,
                {
                    "module_name": module_name,
                    "classes": textwrap.indent(
                        "\n".join(klasses), "    ", lambda line: True
                    )
                }
            ) if len(klasses) > 0 else ""
            functions_description = self.edit_from_template(
                function_template_file,
                {
                    "module_name": module_name,
                    "functions": textwrap.indent(
                        "\n".join(functions), "    ", lambda line: True
                    )
                }
            ) if len(functions) > 0 else ""
            module_description = (module.__doc__ or "").split("\n")
            lines = list(
                filter(
                    None,
                    (line.rstrip() for line in module_description)
                )
            )
            module_description = lines[0] if len(lines) > 0 else ""
            module_title = f":mod:`{module_name}`: {module_description}"
            module_title += f"\n{'=' * len(module_title)}"
            info = {
                "module_title": module_title,
                "module_name": module_name,
                "classes": classes_description,
                "functions": functions_description
            }
            self.write_from_template(outfile, info, verbose=self.verbose)

        # Write index
        template_file = os.path.join(
            self.resourcedir, "templates", "modules_index.rst"
        )
        index_file = os.path.join(self.apidir, "index.rst")
        shutil.copy(template_file, index_file)
        info = {
            "project": self.module_name,
            "modules": textwrap.indent(
                "\n".join(sorted(index)), "   ", lambda line: True
            )
        }
        self.write_from_template(index_file, info, verbose=self.verbose)

    @classmethod
    def write_from_template(cls, template_file, template_info, verbose=0):
        """ Edit/save inplace a template file.

        Parameters
        ----------
        template_file: str
            the location of the template file (modified inplace).
        template_info: dict
            a mapping used to edit the template content.
        verbose: int, default 0
            control the verbosity.
        """
        if verbose > 1:
            print(f"[debug] generating file in {template_file}...")
            pprint(template_info)
        with open(template_file) as of:
            buff = of.read()
        with open(template_file, "w") as of:
            of.write(buff.format(**template_info))

    @classmethod
    def edit_from_template(cls, template_file, template_info):
        """ Edit/return a template file.

        Parameters
        ----------
        template_file: str
            the location of the template file (modified inplace).
        template_info: dict
            a mapping used to edit the template content.

        Returns
        -------
        template: str
            the filled template.
        """
        with open(template_file) as of:
            buff = of.read()
        return buff.format(**template_info)
