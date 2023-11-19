""" Loads General Program configuration as cfg, boxed """

from typing import Any

from box import Box
import yaml

CONFIG_LOC: str = "configs/pocket_api_access_config.yaml"
env = "dev"


def load_config() -> Box:
    """Function for initial loading of configuration data or reloading it"""
    with open(CONFIG_LOC, encoding="utf-8") as fp:
        full_cfg: dict[str, Any] = yaml.safe_load(fp)

    a_cfg: Box = Box(
        {**full_cfg["base"], **full_cfg[env]}, default_box=True, default_box_attr=None
    )

    return a_cfg


cfg: Box = load_config()
