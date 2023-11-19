""" Set-up Logging and load logging configuration as log_cfg, boxed """

import logging
from os import makedirs, path
from typing import Any

from yaml import safe_load
from box import Box

from src.config.config_main import cfg


def load_log_config() -> Box:
    """
    Load logging config as log_cfg
    Create logging folder if necessary
    """
    logging_config_path_filename: str = cfg.LOGGING.CONFIG_PATH

    try:
        with open(file=logging_config_path_filename, mode="r", encoding="UTF-8") as fp:
            log_config_dict: dict[str, Any] = safe_load(fp)  # YAML

        a_log_cfg: Box = Box(
            {**log_config_dict["base"]}, default_box=True, default_box_attr=None
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Log yaml configuration file not found in {logging_config_path_filename}"
        )

    makedirs(name=a_log_cfg.handler.log_file.folder, exist_ok=True)

    return a_log_cfg


log_cfg: Box = load_log_config()

log_fmt = logging.Formatter(fmt=log_cfg.format.simple, style="{")
logging.basicConfig(
    format=log_cfg.format.simple, style="{", datefmt=log_cfg.format.datefmt
)

logger: logging.Logger = logging.getLogger("Exercise File Analysis Logger")
logger.setLevel(level=log_cfg.level)
logger.propagate = False

if log_cfg.handler.console.enabled:
    # Set-up console logger to sys.err
    ch = logging.StreamHandler()
    ch.setLevel(level=log_cfg.handler.console.level)
    ch.setFormatter(fmt=log_fmt)
    logger.addHandler(hdlr=ch)

if log_cfg.handler.log_file.enabled:
    # Set-up file logging
    fh = logging.FileHandler(
        filename=path.join(
            log_cfg.handler.log_file.folder, log_cfg.handler.log_file.filename
        )
    )
    fh.setLevel(level=log_cfg.handler.log_file.level)
    fh.setFormatter(fmt=log_fmt)
    logger.addHandler(hdlr=fh)
