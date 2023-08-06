"""This modules has functions to manipulate and generate standardized json files"""
import json
import os
from pathlib import Path
from typing import Any, TextIO

# This function creates the json file with
# filename and a json string
# Author: Felipe P. Silva
# E-mail: felipefoz@gmail.com


def validate_json_path(directory_path: Any) -> None:
    """Validate Path """
    if os.path.isdir(directory_path) and any(File.endswith(".json") for File in os.listdir(directory_path)):
        print('Invalid Directory or no JSON files found in the directory')


# badge format = {"schemaVersion":1,"label":"hello","message":"sweet world","color":"orange"}
def print_json(label: str, message: str, color: str) -> dict:
    """Returns a JSON (Dict) in the format used by shields.io to create badges"""
    payload = {"schemaVersion": 1, "label": label, "message": message, "color": color}
    return payload


def json_badge(directory_path, filename: str, json_string: dict) -> None:
    """Write to JSON file to disk to the specified directory"""
    print("Creating JSON Badge file for", json_string['label'], "...", end=" ")
    # Using Path function for a platform independent code
    directory_path = Path(directory_path)
    filename = filename + ".json"
    file_to_write = directory_path / filename
    # Write to json file
    outfile: TextIO
    with open(file_to_write, 'w', encoding="utf-8") as outfile:
        json.dump(json_string, outfile)
    outfile.close()
    print("Done!")
