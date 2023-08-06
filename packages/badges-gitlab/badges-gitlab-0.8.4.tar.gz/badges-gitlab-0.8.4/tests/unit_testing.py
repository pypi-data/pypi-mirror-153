import os
import re
import shutil
import sys
import unittest
from io import StringIO
from unittest.mock import patch

import vcr
import xmlrunner

from junitparser import TestSuite

from src.badges_gitlab import __version__ as version
from src.badges_gitlab import badges_api, badges_json, badges_static, badges_svg, badges_test, cli, read_pyproject

fixture_directory_not_exists = os.path.join(os.getcwd(), 'tests', 'test_not_exist')
fixture_json = os.path.join(os.getcwd(), 'tests', 'json')
fixture_svg_location = os.path.join(os.getcwd(), 'tests', 'svg')


class TestAPIBadges(unittest.TestCase):

    def test_validate_path(self):
        expected_value = 'Directory  {}  created!\n'.format(fixture_directory_not_exists)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            badges_api.validate_path(fixture_directory_not_exists)
            self.assertEqual(fake_out.getvalue(), expected_value)

    def tearDown(self) -> None:
        shutil.rmtree(fixture_directory_not_exists)


class TestBadgesJSON(unittest.TestCase):

    def test_print_json(self):
        expects = {"schemaVersion": 1, "label": "some", "message": "msg", "color": "different-color"}
        self.assertEqual(badges_json.print_json("some", "msg", "different-color"), expects)

    def test_json_badge(self):
        expects = {"schemaVersion": 1, "label": 'some', "message": 'msg', "color": 'different-color'}
        filename = "test"
        os.makedirs(fixture_json, exist_ok=True)
        with patch('sys.stdout', new=StringIO()):
            badges_json.json_badge(fixture_json, filename, expects)
            path_to_assert = os.path.join(fixture_json, '{0}.json'.format(filename))
            self.assertTrue(os.path.isfile(path_to_assert), 'Path tested was {0}'.format(path_to_assert))
        shutil.rmtree(fixture_json)


class TestBadgesSVG(unittest.TestCase):

    def test_replace_space(self):
        string_with_spaces = 'some string with spaces'
        expected_string = 'some_string_with_spaces'
        self.assertEqual(badges_svg.replace_space(string_with_spaces), expected_string)

    def test_validate_json_path(self):
        os.makedirs(fixture_svg_location, exist_ok=True)
        with open(os.path.join(fixture_svg_location, 'some.json'), 'w'):
            self.assertTrue(badges_svg.validate_json_path(fixture_svg_location))
        shutil.rmtree(fixture_svg_location)


class TestCLI(unittest.TestCase):

    def test_cli_parse_args_version(self):
        parser = cli.parse_args(['-V'])
        self.assertTrue(parser.version)

    def test_cli_main_version(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            try:
                sys.argv = ['prog', '-V']
                cli.main()
            except SystemExit:
                pass
            self.assertEqual(fake_out.getvalue(), 'badges-gitlab v{0}\n'.format(version) )

    def test_cli_parse_args_badges(self):
        parser = cli.parse_args(['-s','conventional commits', '1.0.1', 'yellow'])
        expected_result = [['conventional commits', '1.0.1', 'yellow']]
        self.assertEqual(parser.static_badges, expected_result)

    def test_cli_parse_args_link_badges(self):
        parser = cli.parse_args(['-lb','https://img.shields.io/pypi/v/badges-gitlab',
                                  'https://img.shields.io/pypi/wheel/badges-gitlab'])
        expected_result = ['https://img.shields.io/pypi/v/badges-gitlab',
                           'https://img.shields.io/pypi/wheel/badges-gitlab']
        self.assertEqual(parser.link_badges, expected_result)

class TestBadgesTest(unittest.TestCase):

    json_test_directory = 'tests/fixtures'

    def test_create_badges_test(self):
        test_file_does_not_exist = unittest.TestCase.subTest
        with test_file_does_not_exist(self):
            xml_path = 'tests/report_not_exist.xml'
            self.assertEqual(badges_test.create_badges_test(self.json_test_directory, xml_path), 'Junit report file does not exist...skipping!')

        test_wrong_file_type = unittest.TestCase.subTest
        with test_wrong_file_type(self):
            file_path = 'Pipfile'
            self.assertEqual(badges_test.create_badges_test(self.json_test_directory, file_path), 'Error parsing the file. Is it a JUnit XML?')

        test_create_badges = unittest.TestCase.subTest
        with patch('sys.stdout', new=StringIO()):
            with test_create_badges(self):
                xml_path = 'tests/fixtures/report.xml'
                regex = re.search(r'Badges from JUnit XML test report tests created!', badges_test.create_badges_test(self.json_test_directory, xml_path))
                self.assertTrue(regex)
        
        test_single_testsuite = unittest.TestCase.subTest
        with patch('sys.stdout', new=StringIO()):
            with test_single_testsuite(self):
                xml_path = 'tests/fixtures/singletestsuite.xml'
                regex = re.search(r'Badges from JUnit XML test report tests created!', badges_test.create_badges_test(self.json_test_directory, xml_path))
                self.assertTrue(regex)

        test_no_testsuites = unittest.TestCase.subTest
        with patch('sys.stdout', new=StringIO()):
            with test_no_testsuites(self):
                xml_path = 'tests/fixtures/notestsuites.xml'
                regex = re.search(r'Badges from JUnit XML test report tests created!', badges_test.create_badges_test(self.json_test_directory, xml_path))
                self.assertTrue(regex)

    def tests_statistics(self):
        stats_tests_dict = {
            'total_tests': 0, 'total_failures': 0, 'total_errors': 0, 
            'total_skipped': 0, 'total_time': 0.4
        }
        testsuite = TestSuite('suite1')
        testsuite.tests = 3
        testsuite.failures = 2
        testsuite.errors = 0
        testsuite.skipped = 0
        testsuite.time = 0.4
        expected_result_dict = {
            'total_tests': 3, 'total_failures': 2, 'total_errors': 0, 
            'total_skipped': 0, 'total_time': 0.8
        }
        test_result = badges_test.tests_statistics(stats_tests_dict, testsuite)
        self.assertEqual(expected_result_dict, test_result)

    def test_create_json_test_badges(self):
        with patch('sys.stdout', new=StringIO()):
            fixture_list = [11, 2, 0, 0, 0.014]
            total_passed = fixture_list[0] - sum(fixture_list[1:4])
            regex = re.search(r'Total Tests = {}, Passed = {}, Failed = {}, '
                              r'Errors = {}, Skipped = {}, Time = {:.2f}s.'.format(fixture_list[0], total_passed,
                                                                             fixture_list[1], fixture_list[2],
                                                                             fixture_list[3],fixture_list[4]),
                              badges_test.create_test_json_badges(self.json_test_directory, fixture_list))
            self.assertTrue(regex)

    def tearDown (self):
        files = os.listdir(self.json_test_directory)
        for file in files:
            if file.endswith('.json'):
                os.remove(os.path.join(self.json_test_directory, file))

class TestReadPyProject(unittest.TestCase):
    fixture_pyproject = os.path.join('tests', 'fixtures')

    def test_pyproject_exists(self):
        target = os.path.join(self.fixture_pyproject, 'pyproject.toml')
        self.assertTrue(read_pyproject.pyproject_exists(target))

    def test_load_pyproject(self):
        test_wrong_file_type = unittest.TestCase.subTest
        with test_wrong_file_type(self):
            target = os.path.join(self.fixture_pyproject, 'pyproject_wrong.toml')
            with patch('sys.stdout', new=StringIO()) as fake_out:
                read_pyproject.load_pyproject(target)
                self.assertEqual(fake_out.getvalue(), 'Incompatible .toml file!\n')

        test_section_not_found = unittest.TestCase.subTest
        with test_section_not_found(self):
            target = os.path.join(self.fixture_pyproject, 'pyproject_no_section.toml')
            with patch('sys.stdout', new=StringIO()) as fake_out:
                read_pyproject.load_pyproject(target)
                self.assertEqual(fake_out.getvalue(), 'The "badges_gitlab" '
                                                      'section in pyproject.toml was not found!\n')

class TestBadgesStatic(unittest.TestCase):

    def test_convert_to_snake_case(self):
        test_word = "label test"
        expected_result = "label_test"
        result = badges_static.to_snake_case(test_word)
        self.assertEqual(result, expected_result)

    def test_convert_list_json_badge(self):
        test_list_ok = unittest.TestCase.subTest
        with test_list_ok(self):
            badges_list = [["label test", "msgtest", "green"],
                         ["label 2test", "msgtest", "blue"]]
            expected_result = [{'schemaVersion': 1, 'label': 'label test', 'message': 'msgtest', 'color': 'green'},
                               {'schemaVersion': 1, 'label': "label 2test", 'message': 'msgtest', 'color': 'blue'}]
            result = badges_static.convert_list_json_badge(badges_list)
            self.assertEqual(result, expected_result)

        test_list_wrong = unittest.TestCase.subTest
        with test_list_wrong(self):
            json_list = ['some','weird','list', 'not compatible']
            expected_result = []
            result = badges_static.convert_list_json_badge(json_list)
            self.assertEqual(result, expected_result)

    def test_print_static_badges(self):
        fixtures_dir = 'tests/fixtures/static/'
        os.makedirs(fixtures_dir, exist_ok=True)
        badge_result = ['label test', 'msg test',  'green']
        badges_list = [badge_result]
        with patch('sys.stdout', new=StringIO()) as fake_out:
            badges_static.print_static_badges(fixtures_dir, badges_list)
            self.assertEqual(fake_out.getvalue(), 'Creating JSON Badge file for label test ... Done!\n')
        shutil.rmtree(fixtures_dir)

    def test_extract_svg_title(self):
        test_file_ok = unittest.TestCase.subTest
        with test_file_ok(self):
            fixture_svg = os.path.join('tests', 'fixtures', 'badge.svg')
            expected_result = 'conventional_commits'
            with open(fixture_svg) as svg_file:
                result = badges_static.extract_svg_title(svg_file.read())
                self.assertEqual(result, expected_result)

        test_file_wrong = unittest.TestCase.subTest
        with test_file_wrong(self):
            fixture_svg = os.path.join('tests', 'fixtures', 'report.xml')
            expected_result = ''
            with open(fixture_svg) as svg_file:
                result = badges_static.extract_svg_title(svg_file.read())
                self.assertEqual(result, expected_result)

    @vcr.use_cassette()
    def test_download_badges(self):
        test_fixtures_dir = os.path.join('tests', 'fixtures')

        test_link_ok = unittest.TestCase.subTest
        with test_link_ok(self):
            url = ['https://img.shields.io/badge/conventional%20commits-1.0.0-yellow']
            with patch('sys.stdout', new=StringIO()):
                badges_static.download_badges(test_fixtures_dir, url)
                result = os.path.join(test_fixtures_dir, 'conventional_commits.svg')
                self.assertTrue(os.path.isfile(result))
                if os.path.exists(result):
                    os.remove(result)


        test_link_wrong = unittest.TestCase.subTest
        with test_link_wrong(self):
            url = ['https://gitlab.com/felipe_public/badges-gitlab']
            with patch('sys.stdout', new=StringIO()) as fake_out:
                badges_static.download_badges(test_fixtures_dir, url)
                self.assertEqual(fake_out.getvalue(), 'Incompatible link from shields.io links, skipping...\n')


if __name__ == '__main__':
    with open('report.xml', 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)
