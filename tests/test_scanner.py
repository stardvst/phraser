""" Scanner testing module. """

import unittest

from phraser.scanner import Scanner
from phraser.scanner import ENDMARK


class TestScanner(unittest.TestCase):

    def setUp(self):
        self.file = open("tests/inputs/source.txt", "r")

    def tearDown(self):
        self.file.close()

    def test_source(self):
        # get source text from file
        source = self.file.read()
        scanner = Scanner(source)

        # get characters from scanner
        import io
        out = io.StringIO()
        character = scanner.get()
        while True:
            if character.char == ENDMARK:
                break
            out.write(repr(character))
            character = scanner.get()

        # compare!
        self.assertEqual(source, out.getvalue())
