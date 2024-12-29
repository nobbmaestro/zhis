import logging
import os
import pathlib
from dataclasses import dataclass, field
from typing import List

import marshmallow_dataclass
from marshmallow import EXCLUDE

DEFAULT_USER_CONFIG_PATH = os.path.expanduser("~/.config/zhis/config.json")


@dataclass
class DatabaseConfig:
    exclude_commands: List[str] = field(
        default_factory=lambda: [
            "clear",
        ]
    )

    class Meta:
        unknown = EXCLUDE


@dataclass
class Config:
    database: DatabaseConfig = field(default_factory=DatabaseConfig)

    class Meta:
        unknown = EXCLUDE


def load_config(filename: str = DEFAULT_USER_CONFIG_PATH) -> Config:
    try:
        config_schema = marshmallow_dataclass.class_schema(Config)()
        json_string = pathlib.Path(filename).read_text(encoding="utf-8")
        return config_schema.loads(json_string)
    except FileNotFoundError:
        logging.info("User config file not found: %s", filename)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logging.warning("Config parse failed with error: %s", exc)
    return Config()
