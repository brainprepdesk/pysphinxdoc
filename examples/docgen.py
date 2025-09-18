"""
Basic example on how to generate a package documentation
========================================================

In modern software development, documentation is a necessity. Yet,
maintaining up-to-date documentation manually is often neglected due to
time constraints, human error, or shifting priorities. This is where
automatic documentation generation becomes a game-changer.

A simple example of how to document a Python package, here the 'pysphinxdoc'
module itself. Please check the :ref:`user guide <user_guide>` for a more in
depth presentation of all functionalities.


Clone the project to document
-----------------------------
"""

import os
import shutil
import subprocess


repo_dir = "/tmp/pysphinxdoc"
if os.path.isdir(repo_dir):
    shutil.rmtree(repo_dir)
cmd = [
    "git", "clone",
    "https://github.com/AGrigis/pysphinxdoc.git"
]
subprocess.check_call(cmd, cwd=os.path.dirname(repo_dir))
os.environ["PYTHONPATH"] += repo_dir


#############################################################################
# Generate the documentation resources
# ------------------------------------

cmd = [
    f"{repo_dir}/pysphinxdoc/sphinxdoc",
    "-v", "2",
    "-p", repo_dir,
    "-n", "pysphinxdoc"
]
subprocess.check_call(
    cmd,
    env=os.environ
)


#############################################################################
# Compute the html documentation
# ------------------------------

cmd = [
    "make", "html-strict"
]
subprocess.check_call(
    cmd, 
    cwd=f"{repo_dir}/doc",
    env=os.environ
)
