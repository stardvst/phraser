import unittest

from tests.test_scanner import TestScanner
from tests.test_lexer import TestLexer

test_cases = (TestScanner, TestLexer)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_case in test_cases:
        tests = loader.loadTestsFromTestCase(test_case)
        suite.addTests(tests)
    return suite
