##########################################################################
# pysphinxdoc - Copyright (C) AGrigis, 2016 - 2025
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


""" Update the documentation.

Generate the following files:
- maintenance.rst
- license.rst
- contributing.rst

Using either the default description or the one available in the project.
"""

import os
from pathlib import Path
from jinja2 import Template

doc_dir = Path(__file__).parent
template_files = [
    doc_dir / "maintenance.jinja",
    doc_dir / "license.jinja",
    doc_dir / "contributing.jinja",
]
output_files = [
    doc_dir / "maintenance.rst",
    doc_dir / "license.rst",
    doc_dir / "contributing.rst",
]


def main() -> None:
    """ Generate '.rst' files from templates.
    """
    for tplfile, outfile in zip(template_files, output_files):
        inject_with_jinja(tplfile, outfile, context=[])


def inject_with_jinja(
        template_file: Path,
        output_file: Path,
        context: list[dict[str, str]]) -> None:
    """ Render Jinja template given context and write it to an output file.

    Parameters
    ----------
    template_file: str
        path to the Jinja template file.
    output_file: str
        path to the output file.
    context: list of dict
        the context dictionary to render the template.
    """
    with template_file.open() as file:
        template_content = file.read()
    template = Template(template_content)
    rendered_content = template.render(os=os, context=context)
    with output_file.open("w") as file:
        file.write(rendered_content)
    print(f"Template rendered and written to {output_file}.")


if __name__ == "__main__":
    main()
