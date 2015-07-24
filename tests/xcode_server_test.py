#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_xserverpy
----------------------------------

Tests for `xserverpy` module.
"""

import unittest

from xserverpy.lib.xcode_server import XcodeServer


class TestXserverpy(unittest.TestCase):

    def test_throws_error_if_corrupted_params(self):
        with self.assertRaises(Exception):
            XcodeServer()

        with self.assertRaises(RuntimeError):
            XcodeServer(host="host")

        with self.assertRaises(RuntimeError):
            XcodeServer(host="host", user="user")

    def test_throws_error_if_url_is_incorrect(self):
        with self.assertRaises(RuntimeError):
            XcodeServer(host="host", user="user", password="pass")

    def test_succeeds_if_all_items_are_correct(self):
        try:
            XcodeServer(host="https://123.123.123.3", user="user", password="pass")
        except:
            self.fail("")

if __name__ == '__main__':
    unittest.main()
