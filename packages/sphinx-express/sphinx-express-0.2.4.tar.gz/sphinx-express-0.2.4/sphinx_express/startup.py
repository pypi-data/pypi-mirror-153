import pkg_resources
import shutil
from .configs import RECOMEND_MODULES, DEFAULT_CONFIG
from .templates import REPLACE_CONFIGS, APPEND_CONFIGS

def initconfig():
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = RECOMEND_MODULES - installed

    if missing:
        pkgs = " ".join(str(e) for e in missing)
        click.echo("\nYou should install follows packages.")
        click.echo("python -m pip install {}".format(pkgs))

    config = SphinxExpress()
    config_data = config.load_config(DEFAULT_CONFIG)
    config.save_config(config_data)

    os.makedirs(config.default_templatedir, exist_ok=True)
    sphinx_module_dir = os.path.dirname(sphinx.__file__)
    sphinx_template_dir = Path(sphinx_module_dir) / "templates/quickstart"
    files = sphinx_template_dir.glob("*")
    for f in files:
        shutil.copy(f, config.default_templatedir)

    for pattern in REPLACE_CONFIGS.keys():
        config.replace_config_template(pattern, REPLACE_CONFIGS[pattern])

    config.append_config_template(APPEND_CONFIGS)

    click.echo("\nyour configfile: {}".format(config.configfile))
    click.echo("your templatedir: {}".format(config.default_templatedir))
    click.echo("quickstart templates of sphinx into your templatedir.\n")

