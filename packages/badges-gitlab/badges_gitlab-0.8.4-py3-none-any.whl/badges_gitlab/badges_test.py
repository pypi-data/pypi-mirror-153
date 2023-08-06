"""Generate Tests Badges related by parsing JUnit XML files"""
import os

from junitparser import JUnitXml  # type: ignore

from .badges_api import validate_path
from .badges_json import json_badge, print_json


def create_test_json_badges(json_directory, test_results: list) -> str:
    """
    This function returns parses a list with the test summary to json format.
    The list order must be: total tests, total failures, total errors, total_skipped, total_time
    """
    # from the list values we build our dictionary for badges
    total_not_passed = sum(test_results[1:4])
    total_passed = test_results[0] - total_not_passed
    test_badge_color = 'red' if test_results[1] + test_results[2] > 0 else 'green'
    test_badge_summary_text = f'{total_passed} passed, {total_not_passed} failed.' \
        if total_not_passed > 0 else f'{total_passed} passed'
    # define badges dicts
    total_tests_dict = print_json('total tests', str(test_results[0]), 'blue')
    total_time_dict = print_json('total execution time', f'{test_results[4]:.2f}s', 'blue')
    test_summary_dict = print_json('tests', test_badge_summary_text, test_badge_color)
    test_complete_dict = print_json('tests', f'{total_passed} passed, {test_results[1]} failed, '
                                             f'{test_results[2]} errors, {test_results[3]} skipped',
                                    test_badge_color)
    # Dictionary Format = filename : [label, value, color]
    test_badges_dict = {
        "total_tests": total_tests_dict,
        "total_time":  total_time_dict,
        "tests": test_summary_dict,
        "tests_complete": test_complete_dict
    }
    for badge in list(test_badges_dict.keys()):
        json_dict = test_badges_dict[badge]
        json_badge(json_directory, badge, json_dict)
    return f"Total Tests = {test_results[0]}, Passed = {total_passed}, Failed = {test_results[1]}, " \
           f"Errors = {test_results[2]}, Skipped = {test_results[3]}, Time = {test_results[4]:.2f}s.\n" \
           f"Badges from JUnit XML test report tests created!"


def tests_statistics(stats_tests_dict: dict, testsuite) -> dict:
    """This function returns the Test Statistics Dictionary with added
        values from the testsuite.

    Args:
        stats_tests_dict (dict): dictionary with listed tests
        testsuite ([junitparser.junitparser.TestSuite]): a testsuite xml node
        needed for filling the stats tests dicitionary

    Returns:
        dict: returns the stats_tests_dict with the new values.
    """
    stats_tests_dict['total_tests'] += testsuite.tests
    stats_tests_dict['total_failures'] += testsuite.failures
    stats_tests_dict['total_errors'] += testsuite.errors
    stats_tests_dict['total_skipped'] += testsuite.skipped
    stats_tests_dict['total_time'] += testsuite.time

    return stats_tests_dict


def create_badges_test(json_directory, file_path: str) -> str:
    """
    This function parses a JUnit XML file to extract general information
    about the unit tests.
    """
    validate_path(json_directory)
    # Define a dictionary of varibles for using it in functions
    stats_tests_dict = {
        'total_tests': 0,
        'total_failures': 0,
        'total_errors': 0,
        'total_skipped': 0,
        'total_time': 0.0
    }
    if not os.path.isfile(file_path):
        return 'Junit report file does not exist...skipping!'
    try:
        testsuites = JUnitXml.fromfile(file_path)
        if testsuites.name is not None:
            # Append if it only contains one test suite (without <testsuites> node).
            testsuites = [testsuites]
        for testsuite in testsuites:
            tests_statistics(stats_tests_dict, testsuite)
        # Returns json badges for test results from a converted list
        # from dictionaries
        return create_test_json_badges(json_directory, list(stats_tests_dict.values()))

    except SyntaxError:
        return 'Error parsing the file. Is it a JUnit XML?'
