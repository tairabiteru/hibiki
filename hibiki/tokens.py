import dataclasses
import typing as t

from errors import DefinitionError


@dataclasses.dataclass
class Token:
    """
    Defines a token.

    All tokens returned by Hibiki's lexer are subclasses of this.
    Each token has a start, an index denoting where it starts in
    the data stream, and an end, which denotes the same thing...but
    the end.
    """
    start: int
    end: int


@dataclasses.dataclass
class Chord(Token):
    """
    Defines a Chord token

    In Hibiki, chords are defined inside of {}
    So for example, a {C}chord written inline with the {F}lyrics
    would render as the contents of the brace, immediately above
    the next character after the right brace.
    """
    value: str


@dataclasses.dataclass
class Header(Token):
    """
    Defines a Header token

    Headers are the defined in [], and denote the beginning of
    another token called a Section. The brackets encapsulate the
    name of the section which the header defines, like a [Chorus]
    or a [Verse].
    """
    value: str

    def render(self) -> str:
        return f"[{self.value}]\n"


@dataclasses.dataclass
class Char(Token):
    """
    Defines a Char token.

    Sort of exactly what it sounds like, this token defines literally
    everything else not explicitly defined here.
    """
    value: str


@dataclasses.dataclass
class NewLine(Char):
    value: str = "\n"


@dataclasses.dataclass
class Section(Token):
    """
    Defines a Section token
    
    We're getting a bit more contextual here, and this is arguably the job
    of a parser, but if you think that, please reference the following diagram:
    https://preview.redd.it/xtgk541lne141.png?auto=webp&s=495cc368db917b41bdc646f0ab63d9bba8c5d388

    Anyway, a section is analogous to a musical section. Sections consist of a
    Header token, and a list of Char and Chord tokens which make up the body of
    the section.

    This class also keeps track of previously defined sections, as this allows
    us to prevent people from having to violate DRY when typing tabs out.
    """
    ALL = {}
    header: Header
    tokens: t.List[Token]

    def __init__(self, start, end, header, tokens):
        
        # If a header's value is not in the list of all headers,
        # then a section with that header name has never been defined.
        if header.value not in self.ALL:
            super().__init__(start, end)
            self.header = header
            self.tokens = tokens

            # If this section does not have any tokens associated with it, then
            # it's as though it's been typed with its header alone. This is
            # only valid if the header's name matches a previously defined
            # header, which we just proved false, so raise a DefinitionError.
            if all([isinstance(token, NewLine) for token in tokens]):
                raise DefinitionError(f"Empty body reference to undefined header '{header.value}'")

            self.ALL[header.value] = self
        
        # If a header's value IS in this list of all headers,
        # then a section with that header name HAS been defined before.
        else:
            # The only way this is allowed is if the header contains no tokens,
            # as if referring to a previously defined section. If the section
            # has tokens, then you're overwriting a previous section, and this
            # is not allowed.
            if not all([isinstance(token, NewLine) for token in tokens]):
                raise DefinitionError(f"Redefinition of previously defined header '{header.value}'")
            
            tokens = self.ALL[header.value].tokens

            super().__init__(start, end)
            self.header = header
            self.tokens = tokens

    def __repr__(self) -> str:
        return f"<Section [{self.header.value}]>"