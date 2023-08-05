# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Imports -----------------------------------------------------------------
import sys
import os
from datetime import datetime
from importlib.metadata import version as metadata_version

needs_sphinx = '4.1'

# -- Automatic Information ---------------------------------------------------
now = datetime.now()
year = '%d' % now.year

# `production`/`debug` tags
# - Can be used on the document as:
#   .. only:: production
#   .. only:: debug
# - Defaults to debug mode
PRODUCTION = tags.has('production')  # noqa: F821
if not PRODUCTION:
    tags.add('debug')  # noqa: F821

# -- Project information -----------------------------------------------------
project = os.environ['PROJECT']
author = 'Powertools Technologies'
copyright = f'{year}, {author}'

category = 'Miscellaneous'
description = f'{project} Description'

version = metadata_version(project)
release = version if PRODUCTION else 'dev'

# Primary Project Domain
# https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html
primary_domain = 'py'

# -- Project Settings --------------------------------------------------------

# The suffix(es) of source filenames.
source_suffix = {
    '.rst': 'restructuredtext',
    # '.md': 'markdown',
}

# The master toctree document.
root_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    'Thumbs.db',
    '.DS_Store',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Show warnings on the built docs. Useful for debugging
keep_warnings = PRODUCTION is False
# List of warnings to suppress
suppress_warnings = [
]


# Default role
# `txt` is equivalent to :DEFAULT_ROLE:``
default_role = 'any'

today_fmt = '%d %B %Y'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Default highlight language
highlight_language = 'none'

# Automatically number figures (with caption)
numfig = True

# -- Sphinx Extensions ----------------------------------------------------

extensions = []

# InterSphinx
# Link to other Sphinx documentation repositories
extensions.append('sphinx.ext.intersphinx')
python_vi = sys.version_info
intersphinx_mapping = {
    'python': (
        'https://docs.python.org/%d.%d' % (python_vi.major, python_vi.minor),
        None,
    ),
}

# To Do
extensions.append('sphinx.ext.todo')
todo_include_todos = True

# GraphViz
# Use SVG instead of rendering to PNG
extensions.append('sphinx.ext.graphviz')
graphviz_output_format = 'svg'

# Automatically Label Sections
# Add a reference to all document sections.
extensions.append('sphinx.ext.autosectionlabel')
autosectionlabel_prefix_document = True  # Prefix reference with document name

# AutoDoc
extensions.append('sphinx.ext.autodoc')
autodoc_member_order = 'groupwise'
autodoc_default_options = {
    'members': True,
    'show-inheritance': True,
}
autodoc_typehints = 'both'
autodoc_typehints_description_target = 'documented'

# AutoDoc: Napoleon
# Convert Google-style docstring to proper rst metadata
extensions.append('sphinx.ext.napoleon')
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_attr_annotations = True

# AutoSummary
extensions.append('sphinx.ext.autosummary')
autosummary_generate = True
autosummary_generate_overwrite = False

# Auto API Documentation
# - A souped-up version of AutoSummary and AutoDoc
extensions.append('sphinx_automodapi.automodapi')
extensions.append('sphinx_automodapi.smart_resolver')

# Expose slow files
if PRODUCTION:
    extensions.append('sphinx.ext.duration')

# Include GitHub Detritus
extensions.append('sphinx.ext.githubpages')

# Support ToDo
extensions.append('sphinx.ext.todo')
todo_emit_warnings = PRODUCTION is False
todo_include_todos = PRODUCTION is False

# See Also:
# # extensions.append('sphinx.ext.ifconfig')
# # extensions.append('sphinx.ext.doctest')
# https://github.com/wpilibsuite/sphinxext-opengraph
# https://github.com/executablebooks/sphinx-autobuild#readme
# https://github.com/executablebooks/sphinx-copybutton#readme

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'

# Theme: Alabaster (default)
# https://alabaster.readthedocs.io/en/latest/customization.html#theme-options
if html_theme == 'alabaster':
    pass

# Theme: Read the Docs
if html_theme == 'sphinx_rtd_theme':
    html_theme_options = {
        'collapse_navigation': False,
        'navigation_depth': '-1',
        'display_version': True,
        'logo_only': False,
        'prev_next_buttons_location': None,
        'style_external_links': True,
        # 'style_nav_header_background': None,
    }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Don't include the source files in the HTML output
html_copy_source = False

# Base URL locations. To be filled at runtime?
html_baseurl = ''
html_use_opensearch = html_baseurl

manpages_url = 'https://man.archlinux.org/man/{page}.{section}'

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    # "Main" manual page, section 7: Miscellaneous
    (root_doc, project, '%s Documentation' % project, [author], 7)
]
man_show_urls = True
man_make_section_directory = True

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (root_doc, project, f'{project} Documentation', author, project, description, category),
]

# -- Options for linkcheck ------------------------------------------------

# Regexes with ignored URL
linkcheck_ignore = [
]

# Map URL regex to headers to be sent
linkcheck_request_headers = {
    "*": {
        "Accept": "text/html,application/xhtml+xml",
    }
}

# Check `#anchors` in URL, by parsing the result
linkcheck_anchors = True

linkcheck_retries = 5
