from __future__ import annotations
import re
import typing as t

from .utils import replace_all
from .chord import Chord
from .errors import ChordSyntaxError


class Stanza:
    """
    A stanza, or section of text associated with a song.

    A stanza in Hibiki is made up of a name encapsulated in [brackets],
    followed by a new line, some text, and then ended with two consecutive
    line breaks.

    Attributes
    ----------
    text: str
        The text making up the stanza.
    starting_line: int
        The line number where the stanza begins.
    """

    # Regex denoting what a multiplier (ex (x2)) looks like.
    MULTIPLIER_REGEX = r"\(x\d\)\n"

    def __init__(self, text: str, starting_line: int):
        self.text: str = text
        self.starting_line: int = starting_line
        self._recalls = {}

    @classmethod
    def from_match(cls, match: re.Match, starting_line: int) -> Stanza:
        """Instantiate a stanza from an re.Match"""
        return cls(match.group(), starting_line)
    
    @property
    def is_empty(self) -> bool:
        """Shortcut to see if the stanza's body is empty."""
        return len(self.lines) == 0
    
    @property
    def name(self) -> str:
        """
        The name of the stanza
        
        This is what appears inside of the [brackets].
        """
        return replace_all(
            self.text.split("\n")[0],
            "[]", 
            ""
        ).strip()
    
    @property
    def lines(self) -> t.List[Line]:
        """
        A list of Line objects which can be found in the stanza.

        This forms the core function of the stanza class.
        """
        # Buffer to hold lines.
        out: t.List[Line] = []

        # Keep track of the line number.
        # We add 1 because the first line appears after the
        # first line of the stanza.
        line_num = self.starting_line + 1

        for line in filter(lambda e: e != "", self.text.split("\n")[1:]):
            line = line.strip()
            line += "\n"

            # Try to find a multiplier in the line
            match: t.Match[str] | None = re.search(self.MULTIPLIER_REGEX, line)

            # If one exists, we capture the integer from it, remove the
            # multiplier text itself, and then append the line as many
            # times as the multiplier states.
            if match:
                line = line.replace(match.group(), "")
                multiplier: int = int(replace_all(match.group(), "(x)", ""))

                for _ in range(0, multiplier):
                    out.append(Line(self, f"{line}\n", line_num))

            # Otherwise, we just append the line
            else:
                out.append(Line(self, line, line_num))
            
            # Finally, increment the line number
            line_num += 1
        return out


class Space:
    """
    A space or set of spaces found in the chord line.

    At times, it's necessary to denote spaces in the chord line. In particular,
    this occurs when a line's first chord occurs *after* the first lyrics. We
    need a way to know how many spaces there are before the first chord, and
    this class facilitates that.

    Attributes
    ----------
    amount: int
        The number of spaces.
    """
    def __init__(self, amount: int):
        self.amount = amount

    def __str__(self) -> str:
        return self.amount * ' '
    
    def __repr__(self) -> str:
        return f"<Space: {self.amount}>"
    
    @property
    def tab_repr(self) -> str:
        # For duck typing when matching a Chord.
        return str(self)



class Line:
    """
    A single line of source text.
    
    Attributes
    ----------
    stanza: Stanza
        The stanza the line is apart of.
    text: str
        The text making up the line.
    line_num: int
        The line number where the line can be found.
    """
    def __init__(self, stanza: Stanza, text: str, line_num: int):
        self.stanza = stanza
        self.text: str = text
        self.line_num = line_num
    
    def __repr__(self) -> str:
        return f"<Line: {repr(self.text)}>"
    
    def split_chords_and_lyrics(self) -> t.Tuple[t.List[t.Union[Chord, Space]], t.List[str]]:
        """
        Split a line into chords and lyric segments.

        The basic idea behind this function is to split chords
        out from their corresponding lyrics like so:

        ["C",       "F",        "D"]
        ["I like ", "potatoes", "a lot"]

        Essentially, each chord winds up paired to a lyrical segment.
        This makes finding out where the "C" chord goes easy: it goes
        right above the first character of its corresponding segment,
        which is really useful because it massively simplifies the math
        involved in doing this.

        "Isn't the math involved like, basic arithmetic?"

        Shut up.

        (Look, this took me a long time to figure out, okay? I'm still kind
        of salty about it.)

        Anyway, there's a bunch of edge cases involved in doing this
        too, which I'll detail in comments below.
        """
        # Buffers to store Chord objects and lyric segments.
        chords: t.List[t.Union[Chord, Space]] = []
        lyrics: t.List[str] = []

        # First edge case: lines that start with chords.
        # Here we check to see if the line starts with a chord. This is
        # important because if it does, we need to have a way of noting how
        # many spaces there are before the beginning of the first chord. We
        # do that by adding a "Space" object which contains information about
        # how many spaces were there. We'll deal with this later.
        for i in range(0, len(self.text)):
            if self.text[i] == "{":
                if i > 0:
                    chords.append(Space(i))
                break

        # Store the current chord and lyric segment being worked on.
        current_chord: str = ""
        current_lyric: str = ""

        # Flag denoting whether or not we're currently parsing a chord.
        in_chord: bool = False

        # Our column position in the current line. (1 indexed, not 0)
        pos = 1

        for char in self.text:
            if in_chord is True:
                # If we're in a chord and see a {, that shouldn't be possible.
                # This, this is a syntax error.
                if char == "{":
                    raise ChordSyntaxError(self, f"Invalid chord start character in column {pos}")
                
                # If we're in a chord and see a }, then the current chord is
                # ending. So we set in_chord to False and then look up the
                # parsed chord in the database, appending the resultant object
                # to the buffer.
                if char == "}":
                    in_chord = False
                    chords.append(Chord(current_chord))
                    current_chord = ""

                # Otherwise, we continue parsing a new chord.
                else:
                    current_chord += char
            
            else:
                # If we're not parsing a chord and we see }, that shouldn't be
                # possible, so it's a syntax error.
                if char == "}":
                    raise ChordSyntaxError(self, f"Invalid chord start character in column {pos}")

                # If we're not parsing a chord and we see {, then it's the
                # beginning of a new chord.
                if char == "{":
                    in_chord = True

                    # There may be a lyric being parsed, and if so, we need to
                    # append it to the lyrical segments.
                    if current_lyric:
                        lyrics.append(current_lyric)
                    
                    # Since we're ending a chord, reset current_lyric
                    current_lyric = ""
                
                # If we're not parsing a chord, then we simply continue parsing
                # the next lyrical segment.
                else:
                    current_lyric += char
            
            # Increment column position
            pos += 1
        
        # Now we're out of the for loop, so it should not be possible to be
        # inside of a chord still. If we are, it means a chord has not been
        # properly terminated, which is a syntax error.
        if in_chord is True:
            raise ChordSyntaxError(self, f"Invalid chord start character in column {pos}")
        
        # After parsing, it's possible to have the these buffers contain
        # information. (Not as sure about current_chord, but there may be
        # edge cases I haven't thought of.) We make sure these wind up in the
        # final buffers if they are not empty strings.
        if current_chord != "":
            chords.append(Chord(current_chord))
        
        if current_lyric != "":
            lyrics.append(current_lyric)
        
        # Next weird edge case: len(lyrical segments) > len(chords)
        # This can happen when a chord appears after the first lyric, or when
        # a line with only lyrics appears.
        if len(lyrics) > len(chords):
            chords.insert(0, Space(len(lyrics[0])))
        
        # Weird edge case #3: there's more chords than lyric segments.
        # This happens when a line ends with a lonesome chord. Ex:
        # I have a {Cadd9}pota{Dm}to chip  {Am} <----
        # To fix this, we just append an empty string to the lyrics.
        if len(chords) > len(lyrics):
            lyrics.append('')

        # This must be true.
        assert len(lyrics) == len(chords)

        return chords, lyrics
    
    def render_split(self) -> t.Tuple[str, str]:
        """
        Render a single line given its lyrics and chords.

        After separating the chords from lyrics, we can now render the line.
        Again, there's a few edge cases to deal with. Which will be noted.
        """
        chords, lyrics = self.split_chords_and_lyrics()

        # Buffers to store the final chord and lyric line
        chord_line: str = ""
        lyric_line: str = ""

        # Remember when we added "Space" objects if the chord appears after
        # the first lyrics? Now we have to deal with that. If the first chord
        # is a Space object, we remove it and add the spaces onto the chord
        # line, adding the corresponding lyric segment as well.
        if isinstance(chords[0], Space):
            chord_line += chords.pop(0).tab_repr
            lyric_line += lyrics.pop(0)
        
        # Loop through chords, but also lyrics too.
        # Because we ensured they must be the same length, it doesn't really
        # matter which one we use.
        for i in range(0, len(chords)):
            # Three conditions must be observed. First, if the chord's symbol is
            # longer than the lyrical segment. If it is, we append the chord,
            # but then also append the number of missing spaces to the lyrics.
            if len(chords[i].tab_repr) > len(lyrics[i]):
                chord_line += chords[i].tab_repr
                lyric_line += lyrics[i]
                offset = len(chords[i].tab_repr) - len(lyrics[i])
                lyric_line += " " * offset
            
            # Second, if the lyrical segment is longer than the chord's symbol,
            # we basically do the opposite, instead appending spaces to the
            # chord line.
            elif len(lyrics[i]) > len(chords[i].tab_repr):
                lyric_line += lyrics[i]
                chord_line += chords[i].tab_repr
                offset = len(lyrics[i]) - len(chords[i].tab_repr)
                chord_line += " " * offset
            
            # The only remaining case is that they are equal. In which case,
            # all is good in the world. :)
            else:
                chord_line += chords[i].tab_repr
                lyric_line += lyrics[i]
        
        return chord_line.rstrip(), lyric_line.rstrip()
    
    def render(self) -> str:
        # This function mainly serves as a shortcut to render chords and lines
        # together.
        chords, lyrics = self.render_split()
        return f"{chords}\n{lyrics}\n"
