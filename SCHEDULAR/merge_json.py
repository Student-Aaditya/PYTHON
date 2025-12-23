# merge_utils.py
import os
import json
from config import JSON_DIR, MERGED_FILE

def merge_all():
    merged = {}

    for file in os.listdir(JSON_DIR):
        if file.endswith(".json"):
            key = file.replace(".json", "")
            with open(f"{JSON_DIR}/{file}", encoding="utf-8") as f:
                merged[key] = json.load(f)

    with open(MERGED_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, default=str)
