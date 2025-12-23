# json_utils.py
import json
import os
from config import JSON_DIR

os.makedirs(JSON_DIR, exist_ok=True)

def save_table_json(table, data):
    path = f"{JSON_DIR}/{table}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
