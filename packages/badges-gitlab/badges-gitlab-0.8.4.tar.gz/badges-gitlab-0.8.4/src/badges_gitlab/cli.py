"""Main Package File, parses CLI arguments and calls functions"""
import argparse
import os
import sys

from . import __version__ as version
from .badges_api import create_api_badges
from .badges_static import download_badges, print_static_badges
from .badges_svg import print_badges
from .badges_test import create_badges_test
from .read_pyproject import pyproject_config


def parse_args(args):
    """Create arguments and parse them returning already parsed arguments"""
    parser = argparse.ArgumentParser(prog='badges-gitlab',
                                     description=f'Generate Gitlab Badges using JSON files and API requests. '
                                                 f'Program version v{version}.')
    parser.add_argument('-p', '--path', type=str, metavar='PATH', default='',
                        help='path where json and badges files will be generated/located (default: ''./public/badges/)')
    parser.add_argument('-t', '--token', type=str, metavar='TOKEN', default='',
                        help='specify the private-token in command line (default: ${PRIVATE_TOKEN})')
    parser.add_argument('--junit-xml', type=str, metavar='FILE_PATH', default='', dest='junit',
                        help='specify the path of a JUnit XML file for parsing the test results')
    parser.add_argument('-s', '--static-badges', metavar=('LABEL', 'MESSAGE', 'COLOR'),
                        default=[], dest='static_badges', type=str, nargs=3, action='append',
                        help='specify static badges in command line using lists')
    parser.add_argument('-lb', '--link-badges', metavar='URLS', default=[], dest='link_badges',
                        type=str, nargs='+', action='extend', help='specify shields.io urls to download badges')
    parser.add_argument('-V', '--version', action='store_true', help='returns the package version')
    return parser.parse_args(args)


def main() -> None:
    """Main Function for calling arg parser and executing functions"""
    args = parse_args(sys.argv[1:])
    if args.version:
        print(f'badges-gitlab v{version}')
        sys.exit()

    # Read pyproject.toml if the configuration is found
    config_dict = pyproject_config('pyproject.toml')

    # Test for Path, if none are found, chooses public/badges
    if args.path == '':
        if not config_dict.get('path', '') == '':
            args.path = config_dict.get('path')
        else:
            args.path = os.path.join(os.getcwd(), "public", "badges")

    # Assign a environment variable if token was not provided
    if args.token == '':
        if not os.environ.get('PRIVATE_TOKEN') is None:
            args.token = os.environ['PRIVATE_TOKEN']

    # If a Junit File was pointed, executed the junit parser,
    # search in toml as second option
    if not args.junit == '':
        create_badges_test(args.path, args.junit)
    elif not config_dict.get('junit_xml', '') == '':
        toml_junit = config_dict.get('junit_xml', '')
        print(create_badges_test(args.path, toml_junit))

    # Check if there are any static badges to create
    if not args.static_badges == []:
        print_static_badges(args.path, args.static_badges)
    elif not config_dict.get('static_badges', []) == []:
        toml_static_badges = config_dict.get('static_badges', [])
        print_static_badges(args.path, toml_static_badges)

    # Check if there are any link badges to create
    if not args.link_badges == []:
        download_badges(args.path, args.link_badges)
    elif not config_dict.get('link_badges', []) == []:
        toml_link_badges = config_dict.get('link_badges', [])
        download_badges(args.path, toml_link_badges)

    # Call the API Badges Creator
    create_api_badges(args.path, args.token)
    print("Creating badges for files in directory", args.path)
    # Call the SVG Renderer
    print_badges(args.path)


if __name__ == "__main__":
    main()
