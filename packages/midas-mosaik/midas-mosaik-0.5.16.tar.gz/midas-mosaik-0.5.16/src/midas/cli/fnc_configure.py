import logging
import os
from copy import deepcopy
import shutil

import click
from midas.util import runtime_config
from ruamel.yaml import YAML

LOG = logging.getLogger("midas.cli")
DIALOG_1 = (
    "#############\n# MIDAS CLI #\n#############\n"
    "It seems you're using MIDAS for the first time. We need to perform a "
    "short\n"
    "setup. MIDAS will create a folder in your home directory where a "
    "configuration\n"
    "file will be created. Alternatively, the configuration file can be "
    "created in\n"
    "the current directory (but changing the current directory will pop up "
    "this\n"
    "dialog again)."
)
DIALOG_2 = (
    "# STEP 1 #\n"
    "Do you want to create a midas folder in your config directory to store "
    "the\n"
    "configuration file (y|n)?"
)
DIALOG_3 = (
    "# STEP 2 #\n"
    "MIDAS will download the data sets required by certain simulators. "
    "Please\n"
    "provide a path, were the datasets should be stored. Type 'no' if you "
    "don't\n"
    "want to download the datasets (You need to specificy the data path "
    "manually in\n"
    "the newly created runtime-conf.yaml). Type '.' to use the current "
    "directory or\n"
    "specify any other path you like. If you press enter without typing, "
    "the default\n"
    "location will be used (|no|.|<any path you like>):"
)
DIALOG_4 = (
    "# SETUP FINISHED #\n"
    "Make sure you specify the datapath if not done during this setup.\n"
    "Now you can download the datasets using the command 'midasctl "
    "download'.\n"
    "# SUMMARY #"
)


def configure(autocfg=False, update=False, config=None, data_path=None):
    LOG.info("Auto configuration is set to %s.", str(autocfg))

    if (
        autocfg
        and not update
        and any(os.path.exists(f) for f in runtime_config.CONFIG_FILE_PATHS)
    ):
        # A runtime config exists and since we're in autoconfig mode
        # just do nothing
        return
    default_conf = deepcopy(runtime_config.DEFAULT_BASE_CONFIG)
    default_conf_path = runtime_config.CONFIG_FILE_PATHS[1]

    if update:
        config_path = runtime_config.RuntimeConfig()._config_file_path
        if os.path.exists(config_path):
            shutil.copyfile(config_path, f"{config_path}.bak")

        for key, val in runtime_config.RuntimeConfig().paths.items():
            default_conf["paths"][key] = val
        for log_name, log_cfg in (
            runtime_config.RuntimeConfig().logging["loggers"].items()
        ):
            default_conf["logging"]["loggers"][log_name] = dict(log_cfg)
        # default_conf["paths"] = runtime_config.RuntimeConfig()["paths"]
        data_path = runtime_config.RuntimeConfig().paths["data_path"]

    elif not autocfg:
        click.echo(DIALOG_1)
        if config is None:
            rsp = click.prompt(DIALOG_2, default="y")
            if rsp.lower() in ["y", "j", "yes", "ja"]:
                config_path = default_conf_path
            else:
                config_path = os.path.join(
                    os.getcwd(), runtime_config.CONFIG_FILE_NAME
                )
        else:
            config_path = os.path.join(config, runtime_config.CONFIG_FILE_NAME)
        skip_data = False
        if data_path is None:
            rsp = click.prompt(DIALOG_3, default="")

            if len(rsp) > 0:
                if rsp == "no":
                    skip_data = True
                elif rsp == ".":
                    data_path = os.path.abspath(os.getcwd())
                else:
                    try:
                        data_path = os.path.abspath(rsp)
                    except OSError as err:
                        click.echo(
                            "Something went wrong with your path. Please "
                            "restart the program. %s" % err
                        )
                        return False
            else:
                data_path = os.path.split(config_path)[0]
        if not skip_data:
            data_path = os.path.join(
                data_path, runtime_config.DATA_FOLDER_NAME
            )

    else:
        config_path = default_conf_path
        data_path = runtime_config.DEFAULT_BASE_CONFIG["paths"]["data_path"]

    os.makedirs(os.path.split(config_path)[0], exist_ok=True)
    if autocfg and os.path.exists(config_path) and not update:
        # Don't overwrite existing configs if autocfg is activated
        return

    click.echo(DIALOG_4)
    click.echo("Your config will be saved at %s." % config_path)
    click.echo("Your data will be saved at %s." % data_path)
    default_conf["paths"]["data_path"] = data_path
    yml = YAML(typ="safe", pure=True)

    with open(config_path, "w") as cfg_out:
        yml.indent(mapping=2, sequence=4, offset=2)
        yml.dump(default_conf, cfg_out)
