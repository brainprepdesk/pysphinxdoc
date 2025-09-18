##########################################################################
# pysphinxdoc - Copyright (C) AGrigis, 2016 - 2025
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


""" Get the index with highlights.

Generate the following files:
- index.rst

Check for the following files (optional):
- highlights.csv
"""

import csv
import os
from pathlib import Path

from jinja2 import Template

doc_dir = Path(__file__).parent
template_file = doc_dir / "index.jinja"
output_file = doc_dir / "index.rst"
highlights_file = doc_dir / "highlights.csv"


def main() -> None:
    context = []
    if highlights_file.exists():
        with open(highlights_file) as csvfile:
            buff = csv.reader(csvfile, delimiter=",")
            for row in buff:
                print(', '.join(row))
                context.append({
                    "ref": row[0],
                    "thumb": row[1],
                    "tooltip": row[2],
                    "title": row[3],
                })
    inject_with_jinja(template_file, output_file, context=context)


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
