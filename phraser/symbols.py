""" The module for symbol definitions. """

import string

########################################################################
# list of keywords
########################################################################
Keywords = """
if
then
else
elif
endif
while
loop
endloop
print
return
exit
"""
Keywords = Keywords.split()

########################################################################
# list of symbols that are one character long
########################################################################
OneCharacterSymbols = """
=
( )
< >
/ * + -
\\ &
. ;
"""
OneCharacterSymbols = OneCharacterSymbols.split()

########################################################################
# list of symbols that are two character long
########################################################################
TwoCharacterSymbols = """
==
<=
>=
<>
!=
++
**
--
+=
-=
||
"""
TwoCharacterSymbols = TwoCharacterSymbols.split()

IDENTIFIER_STARTCHARS = string.ascii_letters
IDENTIFIER_CHARS = string.ascii_letters + string.digits + "_"

NUMBER_STARTCHARS = string.digits
NUMBER_CHARS = string.digits + "."

STRING_STARTCHARS = "'" + '"'
WHITESPACE_CHARS = " \t\n"

########################################################################
# Token types for things other than keywords and symbols
########################################################################
KEYWORD = 'Keyword'
STRING = "String"
IDENTIFIER = "Identifier"
NUMBER = "Number"
WHITESPACE = "Whitespace"
COMMENT = "Comment"
EOF = "Eof"
