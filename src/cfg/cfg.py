from pydantic import BaseModel, Field, SecretStr
from typing import Optional
import json
from pathlib import Path
from loguru import logger
import sys

global cfg

# Paths
cfg_path = Path(__file__).parent / 'cfg.json'
log_path = Path(__file__).parent / '../../logs/NTB_trace.log'

# Initial logger
logger.remove(0)
logger.add(sys.stdout, format="<green>[{time:ddd DD-MM-YYYY HH:mm:ss.SSS}]</> - <lvl>[{level}]</> - [{module} | {function}] - <bold>{message}</> <dim>{extra}</>", level="TRACE")
logger.add(log_path, format="<green>[{time:ddd DD-MM-YYYY HH:mm:ss.SSS}]</> - <lvl>[{level}]</> - [{module} | {function}] - <bold>{message}</> <dim>{extra}</>", level="TRACE", rotation="5 minutes", retention="1 day")


class Config(BaseModel):  # Config class
    logging_level: str = 'INFO'  # INFO/DEBUG/TRACE

    debug: bool = False  # Debug uses different polling (not webhook) and different api token
    api_token_debug: SecretStr = 'xxx'  # Telegram bot API token used for debug

    api_token: SecretStr = 'xxx'  # Telegram bot API token
    webhook_host: str = 'https://koshy.ru'  # Host where a webhook is located
    webhook_path: str = '/webhook/ninetailedbot'  # Path to webhook

    console_lang: str = 'ru'  # Console language. ru/en but you can add your language in lang folder


def load_config(config_path: Path) -> Config:  # Function to load config
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        return Config(**config_data)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Error parsing JSON from {config_path}: {exc}")
    except Exception as exc:
        raise RuntimeError(f"Unexpected error occurred while loading config: {exc}")


# Config loading
try:
    cfg = load_config(cfg_path)  # loading..
    logger.success(f"Config loaded successfully: {cfg}")

    # changing logger according to cfg file
    logger.remove(1)
    if cfg.logging_level == 'TRACE':
        logger.add(sys.stdout,
                   format="<green>[{time:ddd DD-MM-YYYY HH:mm:ss.SSS}]</> - <lvl>[{level}]</> - [{module} | {function}] - <bold>{message}</> <dim>{extra}</>",
                   level="TRACE")
    elif cfg.logging_level == 'DEBUG':
        logger.add(sys.stdout,
                   format="<green>[{time:ddd DD-MM-YYYY HH:mm:ss.SSS}]</> - <lvl>[{level}]</> - [{module} | {function}] - <bold>{message}</> <dim>{extra}</>",
                   level="DEBUG")
    else:
        logger.add(sys.stdout,
                   format="<green>[{time:ddd DD-MM-YYYY HH:mm:ss.SSS}]</> - <lvl>[{level}]</> - <bold>{message}</> ",
                   level="INFO")

except Exception as e:
    logger.critical(f"Failed to load config: {e}")

