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


########################################################################
# The scanner reads through source and returns one character at a time.
########################################################################
def initialize(text):
    """
    Initialize the scanner.
        :param source: the entire source text
    """
    global source, last_index, current_index, line, column
    source = text
    last_index = len(source) - 1
    current_index = -1
    line = 0
    column = -1


def get():
    """
    Return the next character.
    """
    global last_index, current_index, line, column

    current_index += 1

    if current_index > 0 and source[current_index - 1] == "\n":
        line += 1
        column = -1

    column += 1

    if current_index > last_index:
        char = ENDMARK
    else:
        char = source[current_index]

    return Character(char, line, current_index, column, source)


def lookahead(offset=1):
    """
    Return a string at position current index + offset in source.
        :param offset: offset of requested character from current index.
    """
    global source, current_index, last_index
    if current_index + 1 > last_index:
        return ENDMARK

    return source[current_index + offset]
