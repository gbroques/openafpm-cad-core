# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))

from openafpm_cad_core import _version as project_version  # noqa: E402


# Add lib folder of conda env to sys.path for building docs on Read the Docs
# and importing FreeCAD
on_read_the_dcs = os.environ.get('READTHEDOCS') == 'True'
if on_read_the_dcs:
    conda_lib_path = os.path.join(
        os.environ['CONDA_ENVS_PATH'], os.environ['CONDA_DEFAULT_ENV'], 'lib')
    sys.path.append(conda_lib_path)


def run_apidoc(app):
    """Generate API documentation"""
    from sphinx.ext import apidoc
    max_depth = '1'
    apidoc.main([
        '../openafpm_cad_core',
        '-o', 'openafpm_cad_core',
        '-d', max_depth,
        '--templatedir=_templates/',
        '--force',
        '--no-toc'
    ])


def setup(app):
    app.connect('builder-inited', run_apidoc)


# -- Project information -----------------------------------------------------

project = 'OpenAFPM CAD Core'
author = 'G Roques'

# The full version, including alpha/beta/rc tags
release = project_version.__version__
version = project_version.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'openafpm_cad_core.freecad_spreadsheet'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# A boolean that decides whether module names are prepended to all object names
# (for object types where a “module” of some kind is defined),
# e.g. for py:function directives. Default is True.
add_module_names = False

# -- Auto-doc Options --------------------------------------------------------
autodoc_mock_imports = [
    'FreeCADGui'
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# These folders are copied to the documentation's HTML output
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'styles.css',
]
