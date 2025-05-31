import typing as t

from tokens import Token, Chord, Header, Char, Section


class Lexer:
    def __init__(self, string: str):
        self.pos: int = 0
        self.string: str = string
    
    def advance(self) -> None:
        self.string = self.string[1:]
        self.pos += 1

    @property
    def current(self) -> str:
        return self.string[0]
    
    def lex_section(self) -> Section:
        tokens = []
        if self.current != "[":
            raise ValueError(f"Invalid section beginning '{self.current}'")
        
        start = self.pos

        while True:
            if self.current == "[":
                tokens.append(self.lex_header())
            elif self.current == "\n":
                try:
                    if self.string[1] == "\n":
                        while self.current == "\n":
                            self.advance()
                        return Section(start, self.pos-1, tokens[0], tokens[1:])
                    else:
                        self.advance()
                except IndexError:
                    return Section(start, self.pos, tokens[0], tokens[1:])
            elif self.current == "{":
                tokens.append(self.lex_chord())
            else:
                tokens.append(Char(self.pos, self.pos, self.current))
                self.advance()
    
    def lex_header(self) -> Header:
        header = ""
        start = self.pos
        self.advance()

        while True:
            try:
                if self.current == "]":
                    end = self.pos
                    self.advance()
                    if self.current != "\n":
                        raise ValueError("Unexpected non-EOL while lexing header")
                    break

                else:
                    header += self.current
                    self.advance()
                
            except IndexError:
                raise ValueError("Unexpected EOF while parsing header.")
        
        return Header(start, end, header)
    
    def lex_chord(self) -> Chord:
        VALID = "ABCDEFGmajindsu1234567890"
        chord = ""
        start = self.pos
        self.advance()

        while True:
            try:
                if self.current == "}":
                    end = self.pos
                    self.advance()
                    break

                elif self.current not in VALID:
                    raise ValueError(f"Invalid character in chord: {self.current}")
                else:
                    chord += self.current
                    self.advance()
                
            except IndexError:
                raise ValueError("Unexpected EOF while parsing chord.")
        
        return Chord(start, end, chord)
    
    def lex(self) -> t.List[Token]:
        tokens = []
        while True:
            try:
                tokens.append(self.lex_section())
            except (ValueError, IndexError):
                break
        return tokens