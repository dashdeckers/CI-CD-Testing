"""Sphinx configuration."""
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[1]))

project = "CI-CD-Testing"
author = "Travis Hammond"
copyright = f"2020, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]
