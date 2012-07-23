#!/usr/bin/env python
# encoding: utf-8

import unittest
import os
from jrnl.Journal import Journal
import shutil

# TODO: move test data to a data folder

class TestClasses(unittest.TestCase):
    """Test the behavior of the classes.

        tests related to the Journal and the Entry Classes which can
        be tested withouth command-line interaction
    """

    def setUp(self):
        self.test_data_path = os.path.dirname(os.path.abspath(__file__))
        self.config =   {
                            "timeformat": "%Y-%m-%d %H:%M",
                            "encrypt": False,
                            "tagsymbols": "@",
                            "journal": ""
                        }
        self.config['journal'] = os.path.join(self.test_data_path, 'empty.txt')
        self.journal = Journal(config=self.config)

    def tearDown(self):
        shutil.rmtree(self.journal.data_path)

    def test_data_folder_exists(self):
        self.assertTrue(os.path.exists(self.journal.data_path))
        self.assertTrue(os.path.isdir(self.journal.data_path))

    def test_file_copied(self):
        self.assertEqual(len(os.listdir(self.journal.data_path)), 0)
        with open(os.path.join(self.test_data_path, 'url_test.txt')) as f:
            self.journal.new_entry(f.read())
        self.assertEqual(len(os.listdir(self.journal.data_path)), 1)

    def test_rendering_md(self):
        pass

    def test_rendering_html(self):
        pass

    def test_open_in_browser(self):
        pass

    def test_pathsearch_regex(self):
        true_positive = ['/Volumes/dedan/bla.png',
                         '/Users/dedan/projects/jrnl/tests/golden.jpg',
                         '/Volumes/dedan/test.png',
                         'C:\\a\\windows\\file.png']
        false_positive = ['/Volumes/dedan/bla.blub',
                          'http://en.wikipedia.org/wiki/Generative_model']
        self.config['journal'] = os.path.join(self.test_data_path, 'empty.txt')
        journal = Journal(config=self.config)
        with open(os.path.join(self.test_data_path, 'url_test.txt')) as f:
            results = [res for res in journal.path_search.findall(f.read())]
            for tp in true_positive:
                self.assertIn(tp, results)
            for fp in false_positive:
                self.assertNotIn(fp, results)

class TestCLI(unittest.TestCase):
    """test the command-line interaction part of the program"""

    def setUp(self):
        pass

    def test_something(self):
        """first test"""
        pass


if __name__ == '__main__':
    unittest.main()
