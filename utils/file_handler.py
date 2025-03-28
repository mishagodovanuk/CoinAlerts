# utils/file_handler.py
import json
import os

def load_json(file_path: str) -> dict:
    """
    Loads a JSON file and returns its content as a dict.
    If the file does not exist or is empty, returns an empty dict.
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

def save_json(file_path: str, data: dict) -> None:
    """
    Saves a dict to a JSON file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
