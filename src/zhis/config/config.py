import logging
import os
from dataclasses import dataclass, field
from typing import Optional

import marshmallow_dataclass
import yaml
from marshmallow import EXCLUDE

from zhis.gui.types import GuiConfig

DEFAULT_USER_CONFIG_PATH = os.path.expanduser("~/.config/zhis/config.yml")


@dataclass
class Config:
    gui: GuiConfig = field(default_factory=GuiConfig)

    class Meta:
        unknown = EXCLUDE


def load_config(filename: str = DEFAULT_USER_CONFIG_PATH) -> Config:
    try:
        with open(filename, "r", encoding="utf-8") as stream:
            config_schema = marshmallow_dataclass.class_schema(Config)()
            serialized = yaml.safe_load(stream)
            return config_schema.load(serialized)

    except FileNotFoundError:
        logging.info("User config file not found: %s", filename)

    except Exception as exc:  # pylint: disable=broad-exception-caught
        logging.warning("Config parse failed with error: %s", exc)

    return Config()


def serialize_config(config: Config) -> Optional[str]:
    try:
        config_schema = marshmallow_dataclass.class_schema(Config)()
        return yaml.dump(config_schema.dump(config))

    except Exception as exc:  # pylint: disable=broad-exception-caught
        logging.warning("Config serialization failed with error: %s", exc)

    return None
