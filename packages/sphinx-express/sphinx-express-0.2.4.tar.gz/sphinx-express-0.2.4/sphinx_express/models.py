#!/usr/bin/env python

import os
import yaml
import fileinput
from pathlib import Path
from string import Template

from .configs import DISCARD_OPTIONS
from .startup import initconfig
from .versions import __AUTHOR__, __VERSION__, __LICENSE__

class SphinxExpress(object):
    default_configdir = Path.home() / ".sphinx"
    default_templatedir = default_configdir / "templates/quickstart"
    default_configfile = default_configdir / "quickstartrc"
    default_user = os.getlogin()

    def __init__(self, configfile: Path = None):
        if configfile is None:
            self.configfile = self.default_configfile
        else:
            self.configfile = configfile
            self.default_configfile = configfile
        self.config_templatefile = self.default_templatedir  / 'conf.py_t'

    def load_config(self, defaults=None):
        if defaults:
            if isinstance(defaults, dict):
                config = defaults.copy()
            else:
                config = yaml.load(defaults, Loader=yaml.SafeLoader)
        else:
            config = dict()

        try:
            with open(self.configfile, "r") as f:
                template = Template(f.read())
                interpolated_config = template.safe_substitute(config)
                newconf = yaml.load(interpolated_config, Loader=yaml.SafeLoader)
                config.update(newconf)
        except:
            pass

        return config

    def save_config(self, config: dict, discard_options=DISCARD_OPTIONS):
        for key in discard_options:
            config.pop(key)
        config_dir = os.path.dirname(self.configfile)
        os.makedirs(config_dir, exist_ok=True)
        with open(self.configfile, "w") as f:
            rv = yaml.dump(config, stream=f,
                           default_flow_style=False, sort_keys=False)

    def replace_config_template(self, search_text, replace_text):
        with fileinput.input(self.config_templatefile, inplace=True) as f:
            for line in f:
                new_line = line.replace(search_text, replace_text)
                print(new_line, end='')

    def append_config_template(self, configs):
        f = open(self.config_templatefile, 'a')
        f.write(configs)
        f.close()


