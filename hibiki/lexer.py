import typing as t

from tokens import Chord, Header, Char, Section, NewLine


class Lexer:
    """
    Defines Hibiki's lexer.

    The job of a lexer is to perform tokenization, and Hibiki's lexer is
    no different. It works by iterating through every character in the text,
    attempting to create a section token.

    Attributes
    ----------
    pos : int   | The position of the lexer in the text.
    string: str | The string that the lexer is tokenizing.
    """
    def __init__(self, string: str):
        self.pos: int = 0
        self.string: str = string
    
    def advance(self) -> None:
        """ Advance the lexer by one character."""
        self.string = self.string[1:]
        self.pos += 1

    @property
    def current(self) -> str:
        """The current character."""
        return self.string[0]
    
    def lex_section(self) -> Section:
        """
        Lex a Section token.

        A section token is comprised of a header token, and a series of
        Char and NewLine tokens.
        """
        tokens = []
        if self.current != "[":
            raise ValueError(f"Invalid section beginning '{self.current}'")
        
        start = self.pos
        while self.string:
            # A [ always denotes the start of a header.
            if self.current == "[":
                # If we're lexing a header, we'd expect there to be no tokens
                # lexed so far.
                if len(tokens) == 0:
                    tokens.append(self.lex_header())
                # If there are, the only way that can happen is if the previous
                # header's body was empty. Thus, return a new section, as this
                # constitutes a reprisal of that section.
                else:
                    return Section(start, self.pos, tokens[0], tokens[1:])
            
            # If we're currently on a newline char, then one of two things is true:
            # 1. We're about to end a section.
            # 2. We're about to end a line.
            elif self.current == "\n":
                try:
                    # Case #1: If we look ahead and see another newline, we're
                    # ending a section.
                    if self.string[1] == "\n":
                        # In this event, we want to append a newline, then advance
                        # the lexer until the next char is not a newline.
                        tokens.append(NewLine(start, self.pos))
                        while self.current == "\n":
                            self.advance()
                        # Then mint a new session.
                        return Section(start, self.pos-1, tokens[0], tokens[1:])
                    # Case #2: If we're not, then it's a newline, and we should
                    # append a newline token and advance.
                    else:
                        tokens.append(NewLine(start, self.pos))
                        self.advance()

                # If an IndexError ever occurs, we end the section.
                except IndexError:
                    return Section(start, self.pos, tokens[0], tokens[1:])
            # If we're currently seeing a {, that can only be the beginning
            # of a new chord. So we call lex_chord().
            elif self.current == "{":
                tokens.append(self.lex_chord())
            # If none of the above is the case, then it's a char character.
            else:
                tokens.append(Char(self.pos, self.pos, self.current))
                self.advance()
        
        # If we get here and there's still tokens, it means the file ended
        # before the section end was detected, which basically means the
        # section is over anyway.
        if tokens:
            return Section(start, self.pos, tokens[0], tokens[1:])
        else:
            raise AssertionError("How did you get here?")
    
    def lex_header(self) -> Header:
        """Lex a header token"""
        header = ""
        start = self.pos

        # Start by advancing because we don't in lex_section().
        self.advance()

        # We now KNOW we are inside of a header, and thus our range of expected
        # lexemes is restricted.
        while self.string:
            try:
                # If while in a header, we see a ], then the header is ending.
                if self.current == "]":
                    end = self.pos
                    self.advance()

                    # If while ending a header, the next char after ] is not a
                    # newline, that's not valid.
                    if self.current != "\n":
                        raise ValueError("Unexpected non-EOL while lexing header")
                    self.advance()
                    break
                    
                # Otherwise, what's in the [] is recorded as the header's
                # value.
                else:
                    header += self.current
                    self.advance()
            
            # We should not see an IndexError during this, because it would
            # mean the header was not ended (like '[Header') but the file
            # ended. Obviously, that's nonsense.
            except IndexError:
                raise ValueError("Unexpected EOF while parsing header.")
        
        return Header(start, end, header)
    
    def lex_chord(self) -> Chord:
        """Lex a chord token."""

        # The following characters are valid in a chord.
        VALID = "ABCDEFGmajindsu1234567890"
        
        chord = ""
        start = self.pos

        # Start by advancing because we don't in lex_section().
        self.advance()

        # This works pretty similarly to how lex_header() works, but with
        # {} instead of [], and a few other differences.
        while True:
            try:
                if self.current == "}":
                    end = self.pos
                    self.advance()
                    break
                
                # For example, outside of [], a header can contain anything.
                # But chords have a restricted allowable charset.
                elif self.current not in VALID:
                    raise ValueError(f"Invalid character in chord: {self.current}")
                else:
                    chord += self.current
                    self.advance()
                
            except IndexError:
                raise ValueError("Unexpected EOF while parsing chord.")
        
        return Chord(start, end, chord)
    
    def lex(self) -> t.List[Section]:
        """Begin lexing the string passed to the constructor."""
        tokens = []
        while self.string:
            try:
                tokens.append(self.lex_section())
            except (ValueError, IndexError) as e:
                break
        return tokens