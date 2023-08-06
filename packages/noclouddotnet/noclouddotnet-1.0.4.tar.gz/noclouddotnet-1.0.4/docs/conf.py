#
#  This file is part of NoCloud.Net.
#
#  NoCloud.Net is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later version.
#
#  NoCloud.Net is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
#  PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  NoCloud.Net. If not, see <https://www.gnu.org/licenses/>. 
#


import os
import sys

from logging import WARNING, INFO, DEBUG
from sphinx.util import logging

logger = logging.getLogger(__name__)
#logger.setLevel('DEBUG')

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../'))


# barfs on rtd ...
#try:
#    from importlib.metadata import version as meta_version
#except:
#    from importlib_metadata import version as meta_version
#    
#version = meta_version('noclouddotnet')
with open('../VERSION.txt') as fh:
    version = fh.read().strip()

# allow flask commands to be run within the docs - alas still borked ...
os.environ['FLASK_APP'] = 'noclouddotnet'
os.environ['FLASK_ENV'] = 'test'
os.environ['NOCLOUD_NET_SETTINGS'] = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')

logger.info(os.environ['NOCLOUD_NET_SETTINGS'])

# Supress warnings for docs that aren't used yet
# unused_docs = [
# ]

# General information about the project.
project = 'noclouddotnet'
copyright = '2022, Last Bastion Network Pty Ltd.'

# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'm2r2',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.viewcode',
    'sphinx_git',
    'sphinxcontrib.programoutput',
    'stevedore.sphinxext',
]

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

release = version

# Set the default Pygments syntax
highlight_language = 'yaml'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = False

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = 'static/logo.png'


def setup(app):
    pass

