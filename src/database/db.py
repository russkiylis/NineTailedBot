import sys
from pathlib import Path
import json
from pydantic import BaseModel, Field
from typing import Dict, Any
from loguru import logger

from sql_fox import db_init, add, get, update, delete

db_structure_path = Path(__file__).parent / 'db.json'
db_path = Path(__file__).parent / 'database.db'


db_structure = {
    'Users': {
        'id': {'data_type': 'Integer', 'primary_key': True, 'autoincrement': True},
        'name': {'data_type': 'String_100', 'nullable': False},
        'email': {'data_type': 'String_100', 'nullable': False, 'unique': True},
    },
    'Posts': {
        'id': {'data_type': 'Integer', 'primary_key': True, 'nullable': False, 'unique': True, 'index': True, 'comment': 'id!!!'},
        'user_id': {'data_type': 'Integer', 'nullable': False},
        'title': {'data_type': 'String_100', 'nullable': False, 'default': 'test'},
        'content': {'data_type': 'Text', 'nullable': False},
    }
}


try:
    db_classes = db_init(db_structure, 'SQLite', db_path=db_path)  # Database initialization
    logger.info(db_classes)
    logger.success(f"Database structure loaded successfully: {db_structure}")
except Exception as e:
    logger.critical(f"Failed to load database structure: {e}")
    sys.exit(88)


