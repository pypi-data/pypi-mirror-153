#!/usr/bin/env python

import os
import typer
from typing import Optional, List
from pathlib import Path
from sphinx.cmd.quickstart import ask_user, generate, DEFAULTS

from .models import SphinxExpress


def startup_callback(flag: bool):
    if flag:
        from .startup import initconfig
        initconfig()
        raise typer.Exit()

def version_callback(flag: bool):
    if flag:
        from .versions import __AUTHOR__, __VERSION__, __MYPROG__
        typer.echo(f'\n{__MYPROG__} - Version: {__VERSION__}')
        typer.echo(f'Copyright: 2020- Author: {__AUTHOR__}\n');
        raise typer.Exit()

app = typer.Typer(add_completion=False)

@app.command(help="Create required files for a Sphinx project.")
def quickstart(
    project: Optional[str] = typer.Option(None, '-p', '--project',
                 metavar='PROJECT_NAME',
                 help="project name. \ndefault is basename of PROJECT_DIR."),
    author: str = typer.Option(SphinxExpress.default_user,
                 '-a', '--author',
                 metavar='AUTHOR_NAME',
                 help='author name. default is "{}"'.format(
                                      SphinxExpress.default_user)),
    ver: str = typer.Option('0.0.1', '-v', '--ver',
                 metavar='VERSION',
                 help="version of project."),
    lang: str = typer.Option('ja', '-l', '--lang',
                 metavar='LANG',
                 help="document language."),
    templatedir: Optional[Path] = typer.Option(
                SphinxExpress.default_templatedir,
                '-t', '--templatedir',
                 metavar='TEMPLATE_DIR',
                file_okay=False, resolve_path=True, exists=True,
                help="template directory for template files."),
    define_value: List[str] = typer.Option(None, '-d', '--define',
                 metavar='NAE=VALUE',
                help="define a template variable."),
    configfile: Optional[Path] = typer.Option(
                SphinxExpress.default_configfile,
                '-c', '--configfile',
                 metavar='CONFIG_FILEPATH',
                dir_okay=False, exists=True,
                help="sphinx-express configfile."),
    new: bool = typer.Option(False, '-N', '--new',
                             help="Ignore least configures."),
    setup: bool = typer.Option(False, '--setup',
                             callback=startup_callback,
                             help="Copy templates and exit."),
    project_dir: str = typer.Argument(...),
    version: bool = typer.Option(False, '--version',
                             callback=version_callback, is_eager=True,
                             help="Show version and exit."),
    debug: bool = typer.Option(False, '--debug', hidden=True),
):

    def parse_variables(variable_list):
        dummy = dict()
        for variable in variable_list:
            try:
                name, value = variable.split('=')
                dummy[name] = value
            except ValueError:
                typer.echo(f'Invalid template variable: {variable}')
        return  [f'{k}={v}' for k, v in dummy.items()]

    try:
        dir = Path(project_dir)
    except TypeError:
        click.echo("\nError: Missing argument 'PROJECT_DIR'.\n\n", err=True)
        raise typer.Exit()

    if not dir.exists():
        dir.mkdir()
    elif dir.is_dir() is not True:
        click.echo("\nError: Your select  project root is already exists. file: {}".format(project_dir), err=True)
        raise typer.Exit()

    d = DEFAULTS.copy()
    d["path"] = project_dir
    d["project"] = project or os.path.basename(project_dir)

    if lang not in ['en', 'ja']:
        try:
            test_import = f"from sphinx.locale import {lang}"
            eval(test_import)
        except ImportError:
            click.echo(f"{lang} is not supported language, using 'en' instead.")
            lang='en'

    if new:
        templatedir = None
        d["author"] = author
        d["version"] = ver
        d["lang"] = lang
        d["variables"] = parse_variables(list(define_value))
    else:
        config = SphinxExpress(configfile)
        least_config = config.load_config()
        least_variable = set(d.get("variables", []))
        define_value = set(define_value)
        d["variables"] = parse_variables(list(least_variable | define_value))
        d.update(**least_config)

    ask_user(d)

    generate(d, templatedir=templatedir)

    config.save_config(d)

if __name__ == "__main__":
    app()
