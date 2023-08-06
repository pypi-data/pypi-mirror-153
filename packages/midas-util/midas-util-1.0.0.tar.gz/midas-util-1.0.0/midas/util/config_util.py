import os
from typing import Any, Dict, List

from ruamel.yaml import YAML

from . import LOG
from .dict_util import update
from .runtime_config import RuntimeConfig


def get_config_files(configs: List[str], default_path: str) -> List[str]:
    """Collection all scenario configuration files.

    The functions looks at the two default location for scenario files,
    i.e., the `config` folder inside the `scenario` module and the
    `midas_scenario` folder defined in the current runtime config.
    Additionally, every custom config provided with the *configs*
    parameter is checked for presence.

    Parameters
    ----------
    configs: list
        A list containing path-like strings pointing to scenario
        configuration files each.

    Returns
    -------
    list:
        A list of absolute paths to all existing configuration files.

    """

    os.makedirs(default_path, exist_ok=True)

    files = [os.path.join(default_path, f) for f in os.listdir(default_path)]
    user_path = os.path.abspath(RuntimeConfig().paths["scenario_path"])
    os.makedirs(os.path.abspath(user_path), exist_ok=True)
    files.extend([os.path.join(user_path, f) for f in os.listdir(user_path)])

    if configs is not None:
        for ccfg in configs:
            if not ccfg.endswith(".yml"):
                ccfg = f"{ccfg}.yml"
            ccfg = os.path.abspath(ccfg)
            if os.path.isfile(ccfg):
                LOG.debug("Adding custom config at '%s'.", ccfg)
                files.append(ccfg)
            else:
                LOG.warning("Did not found config '%s'.", ccfg)

    return files


def load_configs(files: str) -> Dict[str, Dict[str, Any]]:
    """Load the config files with yaml."""

    configs = dict()
    yaml = YAML(typ="safe", pure=True)
    for path in files:
        if not path.endswith(".yml"):
            continue

        LOG.debug("Loading config file %s.", path)
        with open(path, "r") as yaml_file:
            config = yaml.load(yaml_file)

        if not config:
            LOG.error("Scenario file at '%s' is empty. Skipping!")
            continue

        for key in config:
            if key in configs:
                LOG.critical(
                    "Scenario name with key '%s' does already exist. "
                    "Please choose a different key in file '%s'.",
                    key,
                    path,
                )
                raise ValueError(
                    f"Scenario '{key}' in file {path} is duplicated. "
                    "Please choose a different name."
                )
        update(configs, config)

    return configs


def normalize(params: Dict[str, Any]):
    """Apply some auto corrections for the parameter dictionary.

    Corrects, e.g., the end definition '15*60' to 900.
    The corrections will be performed inplace.

    """
    for key, val in params.items():
        # Search recusively
        if isinstance(val, dict):
            normalize(val)

        # Correct multiplications
        if isinstance(val, str):
            if "*" in val:
                parts = val.split("*")
                product = 1
                try:
                    for part in parts:
                        product *= float(part)

                    if key in ["step_size", "end"]:
                        product = int(product)
                    params[key] = product
                    LOG.debug(
                        "Corrected value for key %s (%s -> %f).",
                        key,
                        val,
                        product,
                    )
                except ValueError:
                    # Not a multiplication
                    pass
            if val.lower() == "true":
                val = True
                LOG.debug(
                    "Corrected value for key %s ('true' -> bool(True)).",
                    key,
                )
            if val.lower() == "false":
                val = False
                LOG.debug(
                    "Corrected value for key %s ('false' -> bool(False)).",
                    key,
                )

        # Correct mosaik params address which is a tuple and not a list
        if key == "mosaik_params":
            if "addr" in val:
                if isinstance(val["addr"], list):
                    LOG.debug("Corrected mosaik_params.")
                    val["addr"] = (val["addr"][0], val["addr"][1])
