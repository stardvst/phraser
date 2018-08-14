""" The starting point of the application. """

import sys
import os

import phraser.symbols as symbols
import phraser.lexer as lexer


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
    with open(output_file, "w") as f:

        print("Here are the characters returned by the lexer:", end='\n')

        lexer.initialize(source)
        while True:
            token = lexer.get()
            writeln(str(token))
            if token.type == symbols.EOF:
                break


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
