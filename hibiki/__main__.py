import sys

from lexer import Lexer


__AUTHOR__ = "Taira"
__VERSION__ = "0.1.0"


try:
    file = sys.argv[1]
except IndexError:
    print("No file input passed.")

with open(file, "r") as infile:
    data = infile.read()
    
    if not data.endswith("\n"):
        data += "\n"


tokens = Lexer(data).lex()
print(tokens)