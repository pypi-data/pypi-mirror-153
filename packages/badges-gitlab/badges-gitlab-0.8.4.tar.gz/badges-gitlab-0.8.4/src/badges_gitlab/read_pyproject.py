"""Read pyproject.toml and import the parameters to be used in the function"""
import os

import toml
from toml.decoder import TomlDecodeError  # type: ignore


def pyproject_exists(file_path: str) -> bool:
    """Verify if the file exists, used internally."""
    return os.path.isfile(file_path)


def load_pyproject(file_path: str) -> dict:
    """
    Load the tool.badges_gitlab section from the toml file.
    Most of the cases it is pyproject.toml because it is hardcoded into main function
    """
    try:
        loaded_file = toml.load(file_path)
        config_dict = loaded_file['tool']['badges_gitlab']
        return config_dict
    except TomlDecodeError:
        print('Incompatible .toml file!')
        return {}
    except KeyError:
        print('The "badges_gitlab" section in pyproject.toml was not found!')
        return {}


def pyproject_config(file_path: str) -> dict:
    """
    Check if the file exists then return the dictionary if it exists
    with the configuration for the badges_gitlab tool
    """
    if not pyproject_exists(file_path):
        return {}
    # if exists, return the dict
    return load_pyproject(file_path)
