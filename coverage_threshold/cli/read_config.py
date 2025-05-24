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
        toml_dict = toml.load(config_file_name)
        try:
            # PEP 518 compliant version
            config_dict = toml_dict["tool"]["coverage-threshold"]
        except KeyError:
            # Legacy version
            config_dict = toml_dict.get("coverage-threshold", {})
        return Config.parse(config_dict)
    else:
        return Config()
