# pylint: skip-file
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------
import datetime
import os

project = 'Dependency Injection Framework'
copyright = f'2015-{datetime.datetime.now().year}, Cochise Ruhulessin'
author = 'Cochise Ruhulessin'

# The full version, including alpha/beta/rc tags
release = os.getenv('SEMVER_RELEASE') or '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx_copybutton'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}



# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_material'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    #'https://assets.unimatrixcdn.com/themes/sphinx-material/css/style.css',
    'css/style.css',
]


# Material theme options (see theme.conf for more information)
html_show_sourcelink = False
html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}
html_theme_options = {
    'nav_title': project,
    'google_analytics_account': 'UA-XXXXX',
    'color_primary': 'blue',
    'color_accent': 'light-blue',
    'master_doc': False,
    'repo_url': 'https://gitlab.com/unimatrixone/libraries/python-unimatrix/crypto',
    'repo_name': 'View source code',
    'globaltoc_depth': 3,
    'globaltoc_collapse': False,
    'globaltoc_includehidden': False,
}
