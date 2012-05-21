#!/usr/bin/env python
# encoding: utf-8

import unittest

class TestClasses(unittest.TestCase):
    """Test the behavior of the classes.

        tests related to the Journal and the Entry Classes which can
        be tested withouth command-line interaction
    """

    def setUp(self):
        pass

    def test_colon_in_textbody(self):
        """colons should not cause problems in the text body"""
        pass


class TestCLI(unittest.TestCase):
    """test the command-line interaction part of the program"""

    def setUp(self):
        pass

    def test_something(self):
        """first test"""
        pass


if __name__ == '__main__':
    unittest.main()
