import sys

from lexer import Lexer
from renderer import Renderer


__AUTHOR__ = "Taira"
__VERSION__ = "0.1.0"


if __name__ == "__main__":
    try:
        file = sys.argv[1]
    except IndexError:
        print("No file input passed.")

    with open(file, "r") as infile:
        data = infile.read()
        
        if not data.endswith("\n"):
            data += "\n"

    tokens = Lexer(data).lex()
    renderer = Renderer(tokens)

    file = file.split(".")[0]
    with open(f"{file}.txt", "w") as out:
        out.write(renderer.render())