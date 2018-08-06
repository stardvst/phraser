""" The scanner module. """

ENDMARK = "\0"


class Character:
    """
    A generic character class.
    The contained info is available to a token that uses this character.
    """

    def __init__(self, char, line, index, column, source):
        """
        Initialize character info.
            :param char:    the character
            :param line:    line of the character in source
            :param index:   index of the character's position in source
            :param column:  index of column of the character in the line
            :param source:  reference to entire source
        """
        self.char = char
        self.line = line
        self.index = index
        self.column = column
        self.source = source

    def __str__(self):
        """
        Return printable string representation of an object.
        """
        char = self.char
        if char == " ":
            char = "   space"
        elif char == "\n":
            char = "   newline"
        elif char == "\t":
            char = "   tab"
        elif char == ENDMARK:
            char = "   eof"

        return (
            str(self.line).rjust(6) +
            str(self.column).rjust(4) +
            "   " +
            char
        )

    def __repr__(self):
        return self.char


class Scanner:
    """
    The scanner class.
    It reads through source and returns one character at a time.
    """

    def __init__(self, source):
        """
        Initialize the scanner.
            :param source: the entire source text
        """
        self.source = source
        self.last_index = len(source) - 1
        self.current_index = -1
        self.line = 0
        self.column = -1

    def get(self):
        """
        Return the next character.
        """
        self.current_index += 1

        if self.current_index > 0 and \
                self.source[self.current_index - 1] == "\n":
            self.line += 1
            self.column = -1

        self.column += 1

        if self.current_index > self.last_index:
            char = ENDMARK
        else:
            char = self.source[self.current_index]

        return Character(char, self.line, self.current_index,
                         self.column, self.source)

    def lookahead(self, offset=1):
        """
        Return a string at position current index + offset in source.
            :param offset: offset of requested character from current index.
        """
        if self.current_index + 1 > self.last_index:
            return ENDMARK

        return self.source[self.current_index + offset]
