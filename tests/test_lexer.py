""" Lexer testing module. """

import unittest

from phraser.lexer import Lexer


class TestLexer(unittest.TestCase):

    def test_whitespace(self):
        self.assert_scan_result("      ", ['Eof(\x00)'])

    def test_comment(self):
        self.assert_scan_result("/* = false */", ['Comment(/* = false */)',
                                                  'Eof(\x00)'])

    def test_eof(self):
        self.assert_scan_result("\0", ['Eof(\x00)'])

    def test_identifier(self):
        self.assert_scan_result("a b c", ['Identifier(a)',
                                          'Identifier(b)',
                                          'Identifier(c)',
                                          'Eof(\x00)'])

    def test_keyowrd(self):
        self.assert_scan_result(
            "if then else elif endif while loop endloop print return exit",
            ['Keyword(if)',
             'Keyword(then)',
             'Keyword(else)',
             'Keyword(elif)',
             'Keyword(endif)',
             'Keyword(while)',
             'Keyword(loop)',
             'Keyword(endloop)',
             'Keyword(print)',
             'Keyword(return)',
             'Keyword(exit)',
             'Eof(\x00)'])

    def test_number(self):
        self.assert_scan_result("2 10 177", ['Number(2)',
                                               'Number(10)',
                                               'Number(177)',
                                               'Eof(\x00)'])

    def test_string(self):
        self.assert_scan_result("\"a string\"", ['String("a string")',
                                                 'Eof(\x00)'])

    def test_twochar_symbol(self):
        self.assert_scan_result("== <= >= <> != ++ ** -- += -= ||",
                                ['==(==)',
                                 '<=(<=)',
                                 '>=(>=)',
                                 '<>(<>)',
                                 '!=(!=)',
                                 '++(++)',
                                 '**(**)',
                                 '--(--)',
                                 '+=(+=)',
                                 '-=(-=)',
                                 '||(||)',
                                 'Eof(\x00)'])

    def test_onechar_symbol(self):
        self.assert_scan_result("= ( ) < > / * + - \\ & . ;",
                                ['=(=)',
                                 '((()',
                                 ')())',
                                 '<(<)',
                                 '>(>)',
                                 '/(/)',
                                 '*(*)',
                                 '+(+)',
                                 '-(-)',
                                 '\\(\\)',
                                 '&(&)',
                                 '.(.)',
                                 ';(;)',
                                 'Eof(\x00)'
                                 ])

    # generic helper method
    def assert_scan_result(self, source, output):
        lexer = Lexer(source)
        self.assertEqual(lexer.get_list(), output)
