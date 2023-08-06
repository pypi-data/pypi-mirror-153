"""
This module handles generation of static badges read from pyproject.toml or
from command line parameters
"""
import os
import re
from xml.parsers.expat import ExpatError

import requests
import xmltodict  # type: ignore

from .badges_json import json_badge, print_json


def to_snake_case(value) -> str:
    """Convert the label from a badge to snake case"""
    return "_".join(value.lower().split())


def convert_list_json_badge(badges_list: list) -> list:
    """Converts the list of badges list to json format to be printed in the json file"""
    json_list = []
    try:
        for badge in badges_list:
            if isinstance(badge, list):
                json_item = print_json(badge[0], badge[1], badge[2])
                json_list.append(json_item)
            else:
                raise TypeError
        return json_list
    except (KeyError, SyntaxError, TypeError):
        return []


def print_static_badges(directory: str, badges_list: list):
    """Call functions to perform actions in order to write a file with json badge information"""
    badges = convert_list_json_badge(badges_list)
    for badge in badges:
        json_badge(directory, to_snake_case(badge['label']), badge)


def extract_svg_title(xml_svg) -> str:
    """
    Get the raw SVG (XML), convert to dict and retrieve the title
    """
    try:
        xml_svg = xmltodict.parse(xml_svg)
        label_raw = xml_svg['svg']['title']
        label_name = re.match(r'^(.*?):', label_raw)
    except (KeyError, ExpatError):
        return ''
    if label_name:
        return to_snake_case(label_name[1])
    return ''


def download_badges(directory: str, badges_urls: list):
    """
    Get the badges from websites and save it locally.
    Now this was written specifically for shields.io
    but it must be studied to use other websites.
    """
    for badge_url in badges_urls:
        request_data = requests.get(badge_url, allow_redirects=True)
        filename = extract_svg_title(request_data.content)
        if not filename == '':
            complete_filename_path = os.path.join(directory, f'{filename}.svg')
            with open(complete_filename_path, 'wb') as svg_file:
                svg_file.write(request_data.content)
            print(f'Downloading {filename} badge... Done!')
        else:
            print('Incompatible link from shields.io links, skipping...')
