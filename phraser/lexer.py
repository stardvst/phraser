""" The lexer module. """

from phraser.scanner import Scanner
from phraser.scanner import ENDMARK
from phraser.token import Token

import phraser.symbols as symbols


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
        while self.c1 in symbols.WHITESPACE_CHARS or self.c2 == "/*":

            # process whitespace
            while self.c1 in symbols.WHITESPACE_CHARS:
                token = Token(self.character)
                token.type = symbols.WHITESPACE
                self.get_char()

                # only if we want lexer to return whitespace
                # return token

            # process comments
            while self.c2 == "/*":
                token = Token(self.character)
                token.type = symbols.COMMENT
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
                return token

        #######################################################################
        # process other tokens
        #######################################################################
        token = Token(self.character)

        # EOF token
        if self.c1 == ENDMARK:
            token.type = symbols.EOF
            return token

        # identifier token
        if self.c1 in symbols.IDENTIFIER_STARTCHARS:
            token.type = symbols.IDENTIFIER
            self.get_char()

            while self.c1 in symbols.IDENTIFIER_CHARS:
                token.value += self.c1
                self.get_char()

            # keyword token
            if token.value in symbols.Keywords:
                token.type = symbols.KEYWORD

            return token

        # number token
        if self.c1 in symbols.NUMBER_STARTCHARS:
            token.type = symbols.NUMBER
            self.get_char()

            while self.c1 in symbols.NUMBER_CHARS:
                token.value += self.c1
                self.get_char()

            return token

        # string token
        if self.c1 in symbols.STRING_STARTCHARS:
            # remember so we can look for it in the end
            quote_char = self.c1

            self.get_char()

            while self.c1 != quote_char:
                if self.c1 == ENDMARK:
                    token.abort("Found EOF before end of string literal")

                token.value += self.c1
                self.get_char()

            token.value += self.c1  # append close quote
            token.type = symbols.STRING
            self.get_char()
            return token

        if self.c2 in symbols.TwoCharacterSymbols:
            token.value = self.c2
            token.type = token.value  # for symbols token is same as value
            self.get_char()  # read past 1st char of 2-char token
            self.get_char()  # read past 2nd char of 2-char token
            return token

        if self.c1 in symbols.OneCharacterSymbols:
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

    def get_list(self):
        tokens = []
        while True:
            token = self.get()
            tokens.append(str(token))
            if token.type == symbols.EOF:
                break
        return tokens
