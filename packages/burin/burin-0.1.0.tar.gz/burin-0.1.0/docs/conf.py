# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join("..", "src")))

onRTD = os.environ.get("READTHEDOCS") == "True"

# -- Project information -----------------------------------------------------

import burin  # noqa: E402
from datetime import datetime  # noqa: E402

docBuildDatetime = datetime.now()

project = burin.__title__
copyright = f"{docBuildDatetime.strftime('%Y')}, {burin.__author__}"
author = burin.__author__
release = burin.__version__
version = release.rpartition(".")[1]

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx"
]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "__pycache__"]
highlight_language = "none"

if not onRTD:
    extensions.append("sphinx_rtd_theme")
    templates_path = ["_templates"]

# -- Options for EPUB output -------------------------------------------------

epub_show_urls = "no"

# -- Options for HTML output -------------------------------------------------

html_theme_options = {}

if not onRTD:
    html_static_path = ["_static"]
    html_theme = "sphinx_rtd_theme"

# -- Options for LaTeX output -------------------------------------------------

latex_engine = "xelatex"
latex_show_pagerefs = True
latex_show_urls = "no"

# -- Options for autodoc -----------------------------------------------------

autoclass_content = "both"

# -- Options for autosectionlabel --------------------------------------------

autosectionlabel_prefix_document = True

# -- Options for autosummary -------------------------------------------------

autosummary_generate = False

# -- Options for intersphinx -------------------------------------------------

intersphinx_mapping = {"python": ('https://docs.python.org/3', None)}
