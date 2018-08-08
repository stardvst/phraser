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

    def __str__(self):
        """
        Return printable string representation of an object.
        """
        return self.type + "(" + self.value + ")"

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
