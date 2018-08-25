""" The parser module. """

import phraser.symbols as symbols
import phraser.lexer as lexer


def quoted(s):
    return '"{0}"'.format(s)


token = None
verbose = False
indent = 0
number_operator = ["+", "-", "*", "/"]


def get_token():
    global token
    if verbose and token:
        print("  " + "(" + str(token) + ")")
    token = lexer.get()


########################################################################
# push and pop
########################################################################
def push(s):
    global indent
    indent += 1
    if verbose:
        # print("  " * indent + " " + s)
        pass


def pop(s):
    global indent
    if verbose:
        # print("  " * indent + " " + s + ".end")
        pass
    indent -= 1


########################################################################
# decorator track0
########################################################################
def track0(func):
    def new_func():
        push(func.__name__)
        func()
        pop(func.__name__)
    return new_func


########################################################################
# decorator track
########################################################################
def track(func):
    def new_func(node):
        push(func.__name__)
        func(node)
        pop(func.__name__)
    return new_func


def error(msg):
    token.abort(msg)


def found_one_of(arg_token_types):
    """
    Returns whether the token is one of the passed types
        :param arg_token_types: list of arg_token_type
    """
    for arg_token_type in arg_token_types:
        if token.type == arg_token_type:
            return True
    return False


def found(arg_token_type):
    if token.type == arg_token_type:
        return True
    return False


def consume(arg_token_type):
    """
    Consume a token of given type and get next token.
    If the current token is not of the expected type,
    raise an error.
        :param arg_token_type: type of token to consume
    """
    # TODO: token.type == symbols.KEYWORD is added to handle "print"; change
    if token.type == arg_token_type or token.type == symbols.KEYWORD:
        get_token()
    else:
        error("Expected to find " + quoted(arg_token_type) +
              " but found " + quoted(token.value))


def parse(source, **kwargs):
    global lexer, verbose
    verbose = kwargs.get("verbose", False)

    # pass the source to lexer
    lexer.initialize(source)
    get_token()
    program()

    if verbose:
        print("~" * 80)
        print("Successful parse!")
        print("~" * 80)

    return ast


########################################################################
# program
########################################################################
@track0
def program():
    """
    program = statement {statement} EOF.
    """
    global ast
    node = Node()

    statement(node)
    while not found(symbols.EOF):
        statement(node)

    consume(symbols.EOF)
    ast = node


########################################################################
# statement
########################################################################
@track
def statement(node):
    """
    statement = print_statement | assignment_statement
    assignment_statement = variable "=" expression ";
    print_statement = "print" expression ";"
        :param node: node containing the token
    """
    if found("print") or token.value == "print":
        print_statement(node)
    else:
        assignment_statement(node)


@track
def print_statement(node):
    """
    print_statement = "print" expression ";"
        :param node: node containing the token
    """
    statement_node = Node(token)
    consume("print")

    node.add_node(statement_node)

    expression(statement_node)
    consume(";")


@track
def assignment_statement(node):
    """
    assignment_statement = variable "=" expression ";
        :param node: node containing the token
    """
    identifier_node = Node(token)
    consume(symbols.IDENTIFIER)

    operator_node = Node(token)
    consume("=")
    node.add_node(operator_node)

    operator_node.add_node(identifier_node)

    expression(operator_node)
    consume(";")


@track
def expression(node):
    """
    expression = string_expression | number_expression
    string_expression = (string_literal | variable) {"||" string_expression}
    number_expression = (number_literal | variable) {number_operator \
        number_expression}
    number_operator = "+" | "-" | "*" | "/"
        :param node: node containing the token
    """
    if found(symbols.STRING):
        string_literal(node)
        while found("||"):
            string_expression(node)

    elif found(symbols.NUMBER):
        number_literal(node)
        while found_one_of(number_operator):
            node.add(token)
            get_token()
            number_expression(node)

    else:
        node.add(token)
        consume(symbols.IDENTIFIER)

        if found("||"):
            while found("||"):
                get_token()
                string_expression(node)
        elif found_one_of(number_operator):
            while found_one_of(number_operator):
                node.add(token)
                get_token()
                number_expression(node)


@track
def string_expression(node):
    """
    string_expression = (string_literal | variable) {"||" string_expression}
        :param node: node containing the token
    """
    if found(symbols.STRING):
        node.add(token)
        get_token()

        while found("||"):
            get_token()
            string_expression(node)
    else:
        node.add(token)
        get_token()
        consume(symbols.IDENTIFIER)

    while found("||"):
        get_token()
        string_expression(node)


@track
def number_expression(node):
    """
    number_expression = (number_literal | variable) {number_operator \
        :param node: node containing the token
        number_expression}
    number_operator = "+" | "-" | "*" | "/"
    """
    if found(symbols.NUMBER):
        number_literal(node)
    else:
        node.add(token)
        consume(symbols.IDENTIFIER)

    while found_one_of(number_operator):
        node.add(token)
        get_token()
        number_expression(node)


def string_literal(node):
    node.add(token)
    get_token()


def number_literal(node):
    node.add(token)
    get_token()


class Node:
    def __init__(self, token=None):
        self.token = token
        self.level = 0
        self.children = []

    def add(self, token):
        """
        Make a node out of token and add it to list of children
            :param token: token to construct a node
        """
        self.add_node(Node(token))

    def add_node(self, node):
        """
        Add the node to the list of children
            :param node: the node to be added to the list
        """
        node.level = self.level + 1
        self.children.append(node)

    def to_string(self):
        s = "    " * self.level

        if self.token is None:
            s += "ROOT\n"
        else:
            s += self.token.value + "\n"

        for child in self.children:
            s += child.to_string()

        return s
