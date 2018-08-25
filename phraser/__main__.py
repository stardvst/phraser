""" The starting point of the application. """

import sys
import os

import phraser.symbols as symbols
import phraser.lexer as lexer
import phraser.parser as parser


########################################################################
# support for writing to output file
########################################################################
def writeln(*args):
    for arg in args:
        f.write(str(arg))
    f.write("\n")


########################################################################
# main
########################################################################
def main(source):
    global f

    ast = parser.parse(source, verbose=True)
    print("~" * 80)
    print("Here is the abstract syntax tree:")
    print("~" * 80)

    with open(output_file, "w") as f:
        f.write(ast.to_string())


########################################################################
# run
########################################################################
if __name__ == "__main__":
    usage = "<program> <input_file> <output_file>"

    # check argc
    if len(sys.argv) < 3:
        print(usage)
        sys.exit()

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # check whether input file exists
    if not os.path.isfile(input_file):
        print("File \"{0}\" does not exist.".format(input_file))
        sys.exit()

    source = open(input_file).read()
    main(source)
    print(open(output_file).read())
