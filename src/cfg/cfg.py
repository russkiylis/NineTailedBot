from pydantic import BaseModel, Field, SecretStr
from typing import Optional
import json
from pathlib import Path


class Config(BaseModel):  # Config class
    debug: bool = False
    api_token_debug: SecretStr = 'xxx'

    api_token: SecretStr = 'xxx'
    webhook_host: str = 'https://koshy.ru'
    webhook_path: str = '/webhook/ninetailedbot'


def load_config(config_path: Path) -> Config:
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        return Config(**config_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON from {config_path}: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error occurred while loading config: {e}")


# Определение пути к файлу конфигурации
cfg_path = Path(__file__).parent / 'cfg.json'

# Загрузка конфигурации
try:
    cfg = load_config(cfg_path)
    print(f"Config loaded successfully: {cfg}")
except Exception as e:
    print(f"Failed to load config: {e}")
