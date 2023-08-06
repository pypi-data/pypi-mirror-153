
RECOMEND_MODULES = {
    "pallets_sphinx_themes",
    "sphinx-rtd-theme",
    "sphinxcontrib-seqdiag",
    "sphinxcontrib-blockdiag",
    "sphinxcontrib-nwdiag",
    "sphinxcontrib-jsmath",
    "sphinxcontrib-runcmd",
    "sphinxcontrib-applehelp",
    "sphinxcontrib-devhelp",
    "sphinxcontrib-htmlhelp",
    "sphinxcontrib-httpdomain",
    "sphinxcontrib-serializinghtml",
    "sphinxcontrib-napoleon",
    "sphinx-charts",
    "recommonmark",
}

DEFAULT_CONFIG = """
sep: true
language: ja
suffix: .rst
master: index
makefile: true
batchfile: true
autodoc: true
doctest: false
intersphinx: false
todo: false
coverage: false
imgmath: true
mathjax: true
ifconfig: true
viewcode: true
project: sample
version: 0.0.1
release: 0.0.1
lang: ja
make_mode: true
ext_mathjax: true
extensions:
- pallets_sphinx_themes
- sphinx_rtd_theme
- sphinx.ext.autodoc
- sphinx.ext.mathjax
- sphinx.ext.autosectionlabel
- sphinxcontrib.blockdiag
- sphinxcontrib.seqdiag
- sphinxcontrib.blockdiag
- sphinxcontrib.nwdiag
- sphinxcontrib.rackdiag
- sphinxcontrib.httpdomain
- sphinxcontrib.runcmd
- recommonmark
mastertocmaxdepth: 2
project_underline: ======
"""

DISCARD_OPTIONS=[
    "rsrcdir",
    "rbuilddir",
    "now",
]
