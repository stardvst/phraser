""" The lexer module. """

import string

from phraser.scanner import Scanner
from phraser.scanner import ENDMARK
from phraser.token import Token

########################################################################
# list of keywords
########################################################################
Keywords = """
if
then
else
elif
endif
while
loop
endloop
print
return
exit
"""
Keywords = Keywords.split()

########################################################################
# list of symbols that are one character long
########################################################################
OneCharacterSymbols = """
=
( )
< >
/ * + -
\\ &
. ;
"""
OneCharacterSymbols = OneCharacterSymbols.split()

########################################################################
# list of symbols that are two character long
########################################################################
TwoCharacterSymbols = """
==
<=
>=
<>
!=
++
**
--
+=
-=
||
"""
TwoCharacterSymbols = TwoCharacterSymbols.split()

IDENTIFIER_STARTCHARS = string.ascii_letters
IDENTIFIER_CHARS = string.ascii_letters + string.digits + "_"

NUMBER_STARTCHARS = string.digits
NUMBER_CHARS = string.digits + "."

STRING_STARTCHARS = "'" + '"'
WHITESPACE_CHARS = " \t\n"

########################################################################
# Token types for things other than keywords and symbols
########################################################################
STRING = "String"
IDENTIFIER = "Identifier"
NUMBER = "Number"
WHITESPACE = "Whitespace"
COMMENT = "Comment"
EOF = "Eof"


class Lexer:
    """ The lexer class. """

    def __init__(self, source):
        """
        Initialize the lexer.
            :param source: the entire source text
        """
        self.c1 = ''
        self.c2 = ''
        self.character = ''

        self.scanner = Scanner(source)

        self.get_char()

    def get(self):
        """
        Construct and return the next token in source.
        """

        #######################################################################
        # process whitespaces and comments
        #######################################################################
        while self.c1 in WHITESPACE_CHARS or self.c2 == "/*":

            # process whitespace
            while self.c1 in WHITESPACE_CHARS:
                token = Token(self.character)
                token.type = WHITESPACE
                self.get_char()

                # only if we want lexer to return whitespace
                # return token

            # process comments
            while self.c2 == "/*":
                token = Token(self.character)
                token.type = COMMENT
                token.value = self.c2

                self.get_char()  # read past 1st char of 2-char token
                self.get_char()  # read past 2nd char of 2-char token

                while not (self.c2 == "*/"):
                    if self.c1 == ENDMARK:
                        token.abort("Found EOF before end of comment")
                    token.value += self.c1
                    self.get_char()

                token.value += self.c2  # append the */ to token

                self.get_char()  # read past 1st char of 2-char token
                self.get_char()  # read past 2nd char of 2-char token

                # only if we want lexer to return comments
                # return token

        #######################################################################
        # process other tokens
        #######################################################################
        token = Token(self.character)

        # EOF token
        if self.c1 == ENDMARK:
            token.type = EOF
            return token

        # identifier token
        if self.c1 in IDENTIFIER_STARTCHARS:
            token.type = IDENTIFIER
            self.get_char()

            while self.c1 in IDENTIFIER_CHARS:
                token.value += self.c1
                self.get_char()

            # keyword token
            if token.value in Keywords:
                token.type = token.value

            return token

        # number token
        if self.c1 in NUMBER_CHARS:
            token.type = NUMBER
            self.get_char()

            while self.c1 in NUMBER_CHARS:
                token.value += self.c1
                self.get_char()

            return token

        # string token
        if self.c1 in STRING_STARTCHARS:
            # remember so we can look for it in the end
            quote_char = self.c1

            self.get_char()

            while self.c1 != quote_char:
                if self.c1 == ENDMARK:
                    token.abort("Found EOF before end of string literal")

                token.value += self.c1
                self.get_char()

            token.value += self.c1  # append close quote
            token.type = STRING
            self.get_char()
            return token

        if self.c2 in TwoCharacterSymbols:
            token.value = self.c2
            token.type = token.value  # for symbols token is same as value
            self.get_char()  # read past 1st char of 2-char token
            self.get_char()  # read past 2nd char of 2-char token
            return token

        if self.c1 in OneCharacterSymbols:
            token.type = token.value  # for symbols token is same as value
            self.get_char()  # read past 1st char of 1-char token
            return token

        # else... we've encountered something we don't recognize
        token.abort(
            "Found unknown character or symbol: \"{0}\"".format(self.c1))

    def get_char(self):
        """
        Get the next character.
        """
        self.character = self.scanner.get()
        self.c1 = self.character.char
        self.c2 = self.c1 + self.scanner.lookahead(1)
