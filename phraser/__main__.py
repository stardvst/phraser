""" The starting point of the application. """

import sys
import os

from phraser.scanner import Scanner
from phraser.scanner import ENDMARK


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

        print("Here are the characters returned by the scanner", end='\n')
        print("   line col character", end='\n')

        scanner = Scanner(source)
        character = scanner.get()
        while True:
            writeln(character)
            if character.char == ENDMARK:
                break
            character = scanner.get()


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
