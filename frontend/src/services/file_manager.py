import json
from pathlib import Path


def read_json(file_path=Path("src/assets/datasets/session_metadata.json")):
    with open(file_path, "r") as file:
        sessions = json.load(file)
    return sessions
