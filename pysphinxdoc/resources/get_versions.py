##########################################################################
# pysphinxdoc - Copyright (C) AGrigis, 2016 - 2025
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


""" Get the documentation URLs.

Generate the following files:
- versions.rst
"""

import os
from pathlib import Path

from jinja2 import Template

doc_dir = Path(__file__).parent
template_file = doc_dir / "versions.jinja"
output_file = doc_dir / "versions.rst"


def main() -> None:
    repo_url = os.popen("git remote -v").read().strip()
    repo_url = repo_url.split("\t")[-1].split(" ")[0].replace(".git", "")
    hub, repo, project = repo_url.split("/")[2: 5]
    if hub == "github.com":
        doc_url = "/".join([f"{repo}.github.io", project])
        doc_url = f"https://{doc_url}"
    else:
        raise AttributeError(
            f"Yet, works only with GitHub repository: {repo_url}."
        )
    release_urls = [
        f"{doc_url}/dev",
        f"{doc_url}/stable",
    ]
    release_urls += [
        f"{doc_url}/{tag.strip().replace('v', '')}"
        for tag in os.popen("git tag").readlines()
    ]
    context = []
    for url in release_urls:
        context.append({"tag": url.split("/")[-1], "url": url})
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
