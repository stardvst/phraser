""" The lexer module. """

from phraser.token import Token

import phraser.symbols as symbols
import phraser.scanner as scanner


def initialize(source):
    """
    Initialize the lexer.
        :param source: the entire source text
    """
    global scanner

    scanner.initialize(source)

    get_char()


def get():
    """
    Construct and return the next token in source.
    """

    #######################################################################
    # process whitespaces and comments
    #######################################################################
    while c1 in symbols.WHITESPACE_CHARS or c2 == "/*":

        # process whitespace
        while c1 in symbols.WHITESPACE_CHARS:
            token = Token(character)
            token.type = symbols.WHITESPACE
            get_char()

            # only if we want lexer to return whitespace
            # return token

        # process comments
        while c2 == "/*":
            token = Token(character)
            token.type = symbols.COMMENT
            token.value = c2

            get_char()  # read past 1st char of 2-char token
            get_char()  # read past 2nd char of 2-char token

            while not (c2 == "*/"):
                if c1 == scanner.ENDMARK:
                    token.abort("Found EOF before end of comment")
                token.value += c1
                get_char()

            token.value += c2  # append the */ to token

            get_char()  # read past 1st char of 2-char token
            get_char()  # read past 2nd char of 2-char token

            # only if we want lexer to return comments
            return token

    #######################################################################
    # process other tokens
    #######################################################################
    token = Token(character)

    # EOF token
    if c1 == scanner.ENDMARK:
        token.type = symbols.EOF
        return token

    # identifier token
    if c1 in symbols.IDENTIFIER_STARTCHARS:
        token.type = symbols.IDENTIFIER
        get_char()

        while c1 in symbols.IDENTIFIER_CHARS:
            token.value += c1
            get_char()

        # keyword token
        if token.value in symbols.Keywords:
            token.type = symbols.KEYWORD

        return token

    # number token
    if c1 in symbols.NUMBER_STARTCHARS:
        token.type = symbols.NUMBER
        get_char()

        while c1 in symbols.NUMBER_CHARS:
            token.value += c1
            get_char()

        return token

    # string token
    if c1 in symbols.STRING_STARTCHARS:
        # remember so we can look for it in the end
        quote_char = c1

        get_char()

        while c1 != quote_char:
            if c1 == scanner.ENDMARK:
                token.abort("Found EOF before end of string literal")

            token.value += c1
            get_char()

        token.value += c1  # append close quote
        token.type = symbols.STRING
        get_char()
        return token

    if c2 in symbols.TwoCharacterSymbols:
        token.value = c2
        token.type = token.value  # for symbols token is same as value
        get_char()  # read past 1st char of 2-char token
        get_char()  # read past 2nd char of 2-char token
        return token

    if c1 in symbols.OneCharacterSymbols:
        token.type = token.value  # for symbols token is same as value
        get_char()  # read past 1st char of 1-char token
        return token

    # else... we've encountered something we don't recognize
    token.abort(
        "Found unknown character or symbol: \"{0}\"".format(c1))


def get_char():
    """
    Get the next character.
    """
    global c1, c2, character
    character = scanner.get()
    c1 = character.char
    c2 = c1 + scanner.lookahead(1)


def get_list():
    tokens = []
    while True:
        token = get()
        tokens.append(str(token))
        if token.type == symbols.EOF:
            break
    return tokens
