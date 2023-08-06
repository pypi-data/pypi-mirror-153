
REPLACE_CONFIGS = {
    "html_theme = 'alabaster'":
"""
# Avilable Themes:
# alabaster, sphinx_rtd_theme
# babel, click, flask, jinja, platter, pocoo, werkzeug
#
html_theme = "sphinx_rtd_theme"
""",
}

APPEND_CONFIGS = """
{%- if 'sphinx.ext.autosectionlabel ' in extensions %}
## True to prefix each section label with the name of the document it is in,
## followed by a colon. For example,
## index:Introduction for a section called Introduction
## that appears in document index.rst.
## Useful for avoiding ambiguity when the same section heading appears
## in different documents.
autosectionlabel_prefix_document = True

## If set, autosectionlabel chooses the sections for labeling by its depth.
## For example, when set 1 to autosectionlabel_maxdepth,
## labels are generated only for top level sections,
## and deeper sections are not labeled. It defaults to None (disabled).
autosectionlabel_maxdepth = 1

{%- endif %}

{%- if 'sphinxcontrib.seqdiag' in extensions %}

# -- Options for seqdiag output -------------------------------------------

# curl -O https://ja.osdn.net/projects/ipafonts/downloads/51868/IPAfont00303.zip
import os
basedir = os.path.abspath(os.path.dirname(__file__))
seqdiag_fontpath = basedir + '/_fonts/IPAfont00303/ipagp.ttf'
seqdiag_html_image_format = 'SVG'
{%- endif %}

{%- if 'sphinxcontrib.nwdiag' in extensions %}

# -- Options for nwdiag output --------------------------------------------

nwdiag_html_image_format = 'SVG'
rackiag_html_image_format = 'SVG'
packetdiag_html_image_format = 'SVG'
{%- endif %}

{%- if 'sphinxcontrib.blockdiag' in extensions %}

# -- Options for blockdiag output ------------------------------------------

blockdiag_html_image_format = 'SVG'
{%- endif %}

{%- if 'sphinxcontrib.actdiag' in extensions %}

# -- Options for actdiag output --------------------------------------------

actdiag_html_image_format = 'SVG'
{%- endif %}

{%- if 'sphinxcontrib.httpdomain' in extensions %}

# -- Options for httpdomain output ------------------------------------------

# List of HTTP header prefixes which should be ignored in strict mode:
http_headers_ignore_prefixes = ['X-']

# Strips the leading segments from the endpoint paths
# by given list of prefixes:
# http_index_ignore_prefixes = ['/internal', '/_proxy']

# Short name of the index which will appear on every page:
# http_index_shortname = 'api'

# Full index name which is used on index page:
# http_index_localname = "My Project HTTP API"

# When True (default) emits build errors when status codes,
# methods and headers are looks non-standard:
http_strict_mode = True
{%- endif %}


{%- if 'recommonmark' in extensions %}

# -- Options for recommonmark output ----------------------------------------
import recommonmark
from recommonmark.transform import AutoStructify

# At the bottom of conf.py
def setup(app):
    app.add_config_value('recommonmark_config', {
            'url_resolver': lambda url: github_doc_root + url,
            'auto_toc_tree_section': 'Contents',
            }, True)
    app.add_transform(AutoStructify)
{%- endif %}

"""
