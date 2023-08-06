"""This VI uses the Gitlab API Functions to create json files for badges"""
import os
from typing import Any

import gitlab  # type: ignore
import iso8601  # type: ignore

from .badges_json import json_badge, print_json

# This function calls the Gitlab API and fetches some project information
# Author: Felipe P. Silva
# E-mail: felipefoz@gmail.com


def validate_path(directory_path: Any) -> None:
    """Validates destination path, if not found, creates it"""
    if not os.path.isdir(directory_path):
        try:
            # Create  Directory MyDirectory
            os.makedirs(directory_path)
            # print if directory created successfully...
            print("Directory ", directory_path, " created!")
        except FileExistsError:
            # print if directory already exists...
            print("Directory ", directory_path, " already exists...")


def issues(project_ref: Any, directory_path: Any) -> None:
    """Retrieves issues count data"""
    # Format :  {'statistics': {'counts': {'all': 30, 'closed': 13, 'opened': 7}}}
    issues_dict = project_ref.issues_statistics.get().statistics['counts']
    json_badge(directory_path, 'issues',
               print_json("issues", str(issues_dict['all']), "blue"))
    json_badge(directory_path, 'open_issues',
               print_json("open issues", str(issues_dict['opened']), "red"))
    json_badge(directory_path, 'closed_issues',
               print_json("closed issues", str(issues_dict['closed']), "green"))


def general_data(project_ref: Any, directory_path: Any) -> None:
    """Retrieves General Data"""
    # Licences may not be found, therefore the Try Function
    try:
        json_badge(directory_path, 'license_key',
                   print_json("license", project_ref.license['key'], "yellow"))
        json_badge(directory_path, 'license_name',
                   print_json("license", project_ref.license['name'], "yellow"))
    except TypeError:
        print("Licenses not found, skipping...")
    finally:
        json_badge(directory_path, 'project_id',
                   print_json("ID", str(project_ref.id), "purple"))
        json_badge(directory_path, 'owner',
                   print_json("owner", project_ref.namespace['name'], "yellow"))
        # noinspection SpellCheckingInspection
        json_badge(directory_path, 'name',
                   print_json("Name", project_ref.name, "yellowgreen"))
        json_badge(directory_path, 'default_branch',
                   print_json("default branch", project_ref.default_branch, "green"))
        created_at = iso8601.parse_date(project_ref.created_at).strftime('%B %Y')
        # noinspection SpellCheckingInspection
        json_badge(directory_path, 'created_at',
                   print_json("created at", created_at, "lightgrey"))
        last_activity_at = iso8601.parse_date(project_ref.last_activity_at).strftime('%-d %B %Y')
        # noinspection SpellCheckingInspection
        json_badge(directory_path, 'last_activity_at',
                   print_json("last activity", last_activity_at, "lightgrey"))
        json_badge(directory_path, 'contributors',
                   print_json("contributors",
                              str(len(project_ref.repository_contributors())), "blue"))
        json_badge(directory_path, 'forks_count',
                   print_json("forks", str(project_ref.forks_count), "orange"))
        # noinspection SpellCheckingInspection
        json_badge(directory_path, 'star_count',
                   print_json("stars", str(project_ref.star_count), "yellowgreen"))


def releases_commits(project_ref: Any, directory_path: Any) -> None:
    """Retrieves Releases, Tags and Commits related data"""
    json_badge(directory_path, 'commits',
               print_json("commits", str(len(project_ref.commits.list(all=True))), "red"))
    last_commit_at = iso8601.parse_date(project_ref.commits.list(all=False)[0].created_at).strftime('%B %Y')
    # noinspection SpellCheckingInspection
    json_badge(directory_path, 'last_commit',
               print_json("last Commit", last_commit_at, "lightgrey"))

    # Test if releases exist
    try:
        json_badge(directory_path, 'release',
                   print_json("release", project_ref.releases.list(all=False)[0].name, "green"))
        released_at = iso8601.parse_date(project_ref.releases.list(all=False)[0].released_at).strftime('%B %Y')
        # noinspection SpellCheckingInspection
        json_badge(directory_path, 'last_release',
                   print_json("last Release", released_at, "lightgrey"))
        json_badge(directory_path, 'releases',
                   print_json("releases", str(len(project_ref.releases.list())), "red"))
    except IndexError:
        print("No releases found, skipping...")
    # Test if tags exist
    try:
        json_badge(directory_path, 'tag',
                   print_json("tag", project_ref.tags.list()[0].name, "green"))
        tag_created_at = iso8601.parse_date(project_ref.tags.list()[0].commit['created_at']).strftime('%B %Y')
        # noinspection SpellCheckingInspection
        json_badge(directory_path, 'last_tag',
                   print_json("last Tag", tag_created_at, "lightgrey"))
    except IndexError:
        print("No tags found, skipping...")


def create_api_badges(directory_path: Any, private_token: str) -> None:
    """Authenticates to API and call the json creation functions"""
    if os.environ.get('CI_SERVER_URL'):
        # Check destination directory and create if needed
        validate_path(directory_path)
        # Authentication
        try:
            gitlab_auth = gitlab.Gitlab(os.environ['CI_SERVER_URL'], private_token=private_token)
            # project id from environment
            project = gitlab_auth.projects.get(int(os.environ['CI_PROJECT_ID']), license='true')
            # Issues Data
            issues(project, directory_path)
            # General Data
            general_data(project, directory_path)
            # Releases and Commit Data
            releases_commits(project, directory_path)
        except gitlab.exceptions.GitlabGetError:
            print('Unable to authenticate, invalid credentials!')
    else:
        print("Invalid environment variables, skipping API Data step!")
