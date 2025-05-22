import os.path
from typing import Optional

import toml

from coverage_threshold.model.config import Config


def read_config(config_file_name: Optional[str]) -> Config:
    DEFAULT_FILENAME = "./pyproject.toml"
    if config_file_name is not None:
        if not os.path.isfile(config_file_name):
            raise FileNotFoundError(f"Config file {config_file_name} not found")
    else:
        config_file_name = DEFAULT_FILENAME
    if os.path.isfile(config_file_name):
        try:
            # PEP 518 compliant version
            return Config.parse(toml.load(config_file_name)["tool"]["coverage-threshold"])
        except KeyError:
            # Legacy version
            return Config.parse(toml.load(config_file_name).get("coverage-threshold", {}))
    else:
        return Config()
