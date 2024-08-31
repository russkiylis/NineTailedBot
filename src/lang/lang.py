from pydantic import BaseModel, Field, SecretStr
from src.cfg.cfg import cfg, logger
from pathlib import Path
import json
import sys

# Paths
lang_path = Path(__file__).parent / f'lang_{cfg.console_lang}.json'


class Lang(BaseModel):  # Language class
    start_0: str = 'start_0'


def load_config(lng_path: Path) -> Lang:  # Function to load language
    if not lang_path.exists():
        raise FileNotFoundError(f"Language file not found: {lng_path}")

    try:
        with open(lng_path, 'r', encoding='utf-8') as f:
            lng_data = json.load(f)
        return Lang(**lng_data)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Error parsing JSON from {lng_path}: {exc}")
    except Exception as exc:
        raise RuntimeError(f"Unexpected error occurred while loading language: {exc}")


# Config loading
try:
    lang = load_config(lang_path)  # loading..
    logger.success(f"Config loaded successfully: {cfg}")

except Exception as e:
    logger.critical(f"Failed to load config: {e}")
