# sphinx-express


## Install

```
$ git clone https://github.com/iisaka51/sphinx-express.git
$ cd sphinx-express
$ python setup.py install
```

## Setup

```bash

$ sphinx-express --setup

You should install follows packages.
python -m pip install sphinx-rtd-theme sphinx-charts pallets_sphinx_themes sphinxcontrib-runcmd sphinxcontrib-napoleon

your configfile: /Users/goichiiisaka/.sphinx/quickstartrc
your templatedir: /Users/goichiiisaka/.sphinx/templates/quickstart
quickstart templates of sphinx into your templatedir.

```

Here is default quickstartrc.

```yaml

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

```

You can change above settings.
and run sphinx-express again.

```bash
$ sphinx-express sample
Welcome to the Sphinx 3.2.1 quickstart utility.

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Selected root path: sample

Creating file /Users/goichiiisaka/docs/sample/source/conf.py.
Creating file /Users/goichiiisaka/docs/sample/source/index.rst.
Creating file /Users/goichiiisaka/docs/sample/Makefile.
Creating file /Users/goichiiisaka/docs/sample/make.bat.

Finished: An initial directory structure has been created.

You should now populate your master file /Users/goichiiisaka/docs/sample/source/index.rst and create other documentation
source files. Use the Makefile to build the docs, like so:
   make builder
where "builder" is one of the supported builders, e.g. html, latex or linkcheck.

```
Usage:

```
$ sphinx-express --help
Usage: sphinx-express [OPTIONS] PROJECT_DIR

  Create required files for a Sphinx project.

Arguments:
  PROJECT_DIR  [required]

Options:
  -p, --project PROJECT_NAME      project name.  default is basename of
                                  PROJECT_DIR.

  -a, --author AUTHOR_NAME        author name. default is "goichiiisaka"
                                  [default: goichiiisaka]

  -v, --ver VERSION               version of project.  [default: 0.0.1]
  -l, --lang LANG                 document language.  [default: ja]
  -t, --templatedir TEMPLATE_DIR  template directory for template files.
                                  [default: /Users/goichiiisaka/.sphinx/templa
                                  tes/quickstart]

  -d, --define NAE=VALUE          define a template variable.
  -c, --configfile CONFIG_FILEPATH
                                  sphinx-express configfile.  [default:
                                  /Users/goichiiisaka/.sphinx/quickstartrc]

  -N, --new                       Ignore least configures.  [default: False]
  --setup                         Copy templates and exit.  [default: False]
  --version                       Show version and exit.  [default: False]
  --help                          Show this message and exit.

```
