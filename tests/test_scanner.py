""" Scanner testing module. """

import unittest

from phraser.scanner import Scanner


class TestScanner(unittest.TestCase):

    def test_space(self):
        self.assert_scan_result(" ", "     0   0      space")

    def test_newline(self):
        self.assert_scan_result("\n", "     0   0      newline")

    def test_tab(self):
        self.assert_scan_result("\t", "     0   0      tab")

    def test_eof(self):
        self.assert_scan_result("\0", "     0   0      eof")

    def test_char(self):
        self.assert_scan_result("a", "     0   0   a")

    # generic helper method
    def assert_scan_result(self, source, output):
        scanner = Scanner(source)
        self.assertEqual(str(scanner.get()), output)
