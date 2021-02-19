import os.path
from typing import Optional

import toml

from coverage_threshold.model.config import Config


def read_config(config_file_name: Optional[str]) -> Config:
    DEFAULT_FILENAME = "./pyproject.toml"
    if config_file_name is not None:
        return Config.parse(toml.load(config_file_name)["coverage-threshold"])
    else:
        if os.path.isfile(DEFAULT_FILENAME):
            return Config.parse(
                toml.load(DEFAULT_FILENAME).get("coverage-threshold", {})
            )
        else:
            return Config()
