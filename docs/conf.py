# docs/conf.py
# txaio documentation configuration - modernized for 2025
import os
import sys
from datetime import datetime

# -- Path setup --------------------------------------------------------------
# Ensures AutoAPI can import the project (src layout)
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../src"))

# Add .cicd/scripts to path for shared Sphinx extensions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.cicd', 'scripts')))

# -- Project information -----------------------------------------------------
project = "txaio"
author = "The WAMP/Autobahn/Crossbar.io OSS Project"
copyright = f"2015-{datetime.now():%Y}, typedef int GmbH (Germany)"

# Dynamically get version from the package
try:
    from txaio import __version__ as release
except Exception:
    release = "dev"

version = release

# -- General configuration ---------------------------------------------------
extensions = [
    # MyST Markdown support
    "myst_parser",

    # Core Sphinx extensions
    "sphinx.ext.autodoc",            # Required by AutoAPI internally
    "sphinx.ext.napoleon",           # Google/NumPy style docstrings
    "sphinx.ext.intersphinx",        # Cross-link other projects
    "sphinx.ext.autosectionlabel",   # {ref} headings automatically
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",           # Link to highlighted source
    "sphinx.ext.ifconfig",           # Conditional content based on config
    "sphinx.ext.doctest",            # Test code examples in documentation

    # Modern UX extensions
    "sphinx_design",                 # Cards, tabs, grids
    "sphinx_copybutton",             # Copy button for code blocks
    "sphinxext.opengraph",           # Social media meta tags
    "sphinxcontrib.images",          # Enhanced image handling
    "sphinxcontrib.spelling",        # Spell checking

    # API documentation (no-import, static analysis)
    "autoapi.extension",

    # Shared WAMP ecosystem extensions (from .cicd submodule)
    "sphinx_auto_section_anchors",   # Stable slug-based HTML anchors
]

# Source file suffixes (both RST and MyST Markdown)
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# The master toctree document
master_doc = "index"

# -- MyST Configuration ------------------------------------------------------
myst_enable_extensions = [
    "colon_fence",        # ::: directive blocks
    "deflist",            # Definition lists
    "tasklist",           # Task lists (- [ ] item)
    "attrs_block",        # Block attributes
    "attrs_inline",       # Inline attributes
    "smartquotes",        # Smart quote substitution
    "linkify",            # Auto-link URLs (requires linkify-it-py)
]
myst_heading_anchors = 3  # Generate anchors for h1-h3

# -- AutoAPI Configuration ---------------------------------------------------
autoapi_type = "python"
autoapi_dirs = ["../src/txaio"]
autoapi_add_toctree_entry = True
autoapi_keep_files = False              # Cleaner RTD builds
autoapi_generate_api_docs = True
autoapi_options = [
    "members",
    "undoc-members",
    "private-members",
    "special-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_ignore = [
    "*/_version.py",
    "*/test_*.py",
    "*/*_test.py",
    "*/conftest.py",
]
autoapi_python_use_implicit_namespaces = True
autoapi_member_order = "alphabetical"   # Predictable ordering

# -- Intersphinx Configuration -----------------------------------------------
# Cross-reference documentation across WAMP ecosystem and dependencies
intersphinx_mapping = {
    # Python Standard Library
    "python": ("https://docs.python.org/3", None),

    # Critical 3rd Party Libraries (txaio-specific)
    "twisted": ("https://docs.twisted.org/en/stable/", None),
}
intersphinx_cache_limit = 5  # Cache remote inventories for 5 days

# -- HTML Output (Furo Theme) ------------------------------------------------
html_theme = "furo"
html_title = f"{project} {release}"

# Furo theme options with Noto fonts and Autobahn subarea colors
html_theme_options = {
    # Source repository links
    "source_repository": "https://github.com/crossbario/txaio/",
    "source_branch": "master",
    "source_directory": "docs/",

    # Noto fonts and Autobahn Medium Blue (#027eae) accent color
    "light_css_variables": {
        "font-stack": "'Noto Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "font-stack--monospace": "'Noto Sans Mono', SFMono-Regular, Menlo, Consolas, monospace",
        "color-brand-primary": "#027eae",
        "color-brand-content": "#027eae",
    },
    "dark_css_variables": {
        "font-stack": "'Noto Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "font-stack--monospace": "'Noto Sans Mono', SFMono-Regular, Menlo, Consolas, monospace",
        "color-brand-primary": "#027eae",
        "color-brand-content": "#027eae",
    },
}

# Logo and favicon (synced from autobahn-python by `just sync-images`)
html_logo = "_static/img/autobahn_logo_blue.svg"
html_favicon = "_static/favicon.ico"

# Static files
html_static_path = ["_static"]
html_css_files = [
    # Load Noto fonts from Google Fonts
    "https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&family=Noto+Sans+Mono:wght@400;500&display=swap",
]

# -- sphinxcontrib-images Configuration --------------------------------------
images_config = {
    "override_image_directive": True,
    "default_image_width": "80%",
}

# -- Spelling Configuration --------------------------------------------------
spelling_lang = "en_US"
spelling_word_list_filename = "spelling_wordlist.txt"
spelling_show_suggestions = True

# -- OpenGraph (Social Media Meta Tags) -------------------------------------
ogp_site_url = "https://txaio.readthedocs.io/en/latest/"

# -- Auto Section Anchors Configuration --------------------------------------
# Force overwrite of auto-generated ids (id1, id2, etc.) with slug-based anchors
auto_section_anchor_force = True

# -- Miscellaneous -----------------------------------------------------------
todo_include_todos = True               # Show TODO items in docs
add_module_names = False                # Cleaner module paths in API docs
autosectionlabel_prefix_document = True # Avoid section label collisions
pygments_style = "sphinx"
pygments_dark_style = "monokai"

# Exclude patterns
exclude_patterns = ["_build", "README.md"]
