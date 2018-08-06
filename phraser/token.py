""" The token module. """


class LexerError(Exception):
    pass


class Token:
    """
    A token is kind of a ting the the lexer returns.
    """

    def __init__(self, start_char):
        """
        Initialize the token.
            :param start_char: the starting character of the token
        """

        self.value = start_char.char

        self.source = start_char.source
        self.line_index = start_char.line
        self.column_index = start_char.column

        # we don't know the type until we;ve processed all characters in token.
        self.type = None

    def show(self, show_line_numbers=False, **kwargs):
        """
        Return printable string representation of an object.
            :param show_line_numbers: show line numbers.
            :param align: show token type left justified with dot leaders.
        """
        tokenTypeLen = 0
        space = ""

        align = kwargs.get("align", True)
        if align:
            tokenTypeLen = 12
            space = " "

        s = ""
        if show_line_numbers:
            s = str(self.line_index).rjust(6) + \
                str(self.column_index).rjust(4) + " "

        if self.type == self.value:
            s = s + "Symbol".ljust(tokenTypeLen, ".") + ":" + space + self.type
        elif self.type == "Whitespace":
            s = s + "Whitespace".ljust(tokenTypeLen, ".") + ":" + space + \
                repr(self.value)
        else:
            s = s + self.type.ljust(tokenTypeLen, ".") + ":" + space + \
                self.value

        return s

    def abort(self, msg):
        """
        Given a message, construct error string based on its position.
            :param msg: error message to print 
        """
        lines = self.source.split("\n")
        current_line = lines[self.line_index]

        raise LexerError("\nIn line " + str(self.line_index + 1) +
                         ", column " + str(self.column_index + 1) + ":\n" +
                         current_line.replace("\t", " ") + "\n" +
                         " " * self.column_index +
                         "^\n" +
                         msg
                         )

    def __repr__(self):
        return self.value
