from sphinx_markdown_parser.parser import MarkdownParser, CommonMarkParser
from sphinx_markdown_parser.transform import AutoStructify
import sphinx_rtd_theme
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

project = 'ejtraderCT'
copyright = '2021, Emerson Pedroso & Douglas Barros'
author = 'Emerson Pedroso & Douglas Barros'

# The full version, including alpha/beta/rc tags
release = '1.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
language = None

master_doc = 'index'

extensions = [
    'sphinx.ext.mathjax',
    'sphinx_js',
    'sphinx_markdown_builder'
]


html_theme = "sphinx_rtd_theme"
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
templates_path = ['_templates']
html_static_path = ['_static']
source_suffix = ['.rst', '.md']


def setup(app):
    app.add_source_suffix('.md', 'markdown')
    app.add_source_parser(MarkdownParser)
    # app.add_source_parser(CommonMarkParser)
    app.add_config_value('markdown_parser_config', {
        'auto_toc_tree_section': 'Content',
        'enable_auto_toc_tree': True,
        'enable_eval_rst': True,
        'enable_inline_math': True,
        'enable_math': True,
    }, True)
    app.add_stylesheet('styles/main.css')
    app.add_javascript('scripts/main.js')
    app.add_transform(AutoStructify)