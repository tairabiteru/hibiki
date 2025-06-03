import dataclasses
import typing as t

from tokens import Token, Chord, Section, NewLine


@dataclasses.dataclass
class Line:
    """
    Defines a line.

    For the purposes of Hibiki's renderer, a line is a list of Chord and Char
    tokens, ended with a single NewLine token.

    Attributes
    ----------
    line_tokens : str | A list of tokens making up the line.
    """
    line_tokens: t.List[Token]

    def reposition(self):
        """
        Reposition lines.

        Hibiki's lexer creates tokens with their absolute position in-file.
        To work with them more locally, we can call this function to overwrite
        their positions to their absolute position in-LINE instead of in-file.
        """
        chords = []
        chars = []

        pos = 0
        chlen = 0
        for token in self.line_tokens:
            if isinstance(token, Chord):
                token.start = pos - chlen
                for _ in token.value:
                    pos += 1
                token.end = pos - chlen
                chlen += token.end - token.start
                chords.append(token)
            else:
                token.start = pos
                token.end = pos
                chars.append(token)
                pos += 1

        return chars, chords
    
    def render_chord_only(self, chords):
        """
        Render a chord-only line.
        
        Lines with only chords in them are rendered according to slightly
        different rules than lines with both chords and chars. Mainly, we
        have to carefully observe spaces between each chord so we don't end
        up with a massive franken-chord like CAm7G#Bbadd9.
        """
        line = []
        pos = 0

        while chords:
            
            chord = chords.pop(0)

            while pos != chord.start:
                if pos > chord.start:
                    offset = pos - chord.start
                    chord.start += offset
                    chord.end += offset
                    for i in range(0, len(chords)):
                        chords[i].start += offset
                        chords[i].end += offset
                else:
                    line.append(" ")
                    pos += 1
            
            for char in chord.value:
                line.append(char)
                pos += 1

            line.append(" ")
            pos += 1
        
        return f"{''.join(line)}\n"

    def render(self):
        """
        Render a line.

        This is the core of Hibiki's function, to render an individual line as
        a properly formatted double-line of chords on top, and lyrics on
        bottom, and BOY WAS THIS REALLY FREAKING HARD.

        Honestly? Don't take my word for it, I'm probably wrong. I have no idea
        how this works.

        Unhappy? Fine, it's magic.
        """
        # When render() is first called, the line's tokens still have their
        # absolute position in-file. reposition() fixes that.
        chars, chords = self.reposition()

        # The length of both the chords line and the lyrics line is whichever
        # of the two ends up being longer.
        line_len = max(
            len(chars),
            sum([len(c.value) for c in chords]) + (len(chords) - 1)
        )

        # Before starting, check to see if the lyric line only contains spaces.
        # If it does, then that's a chord only line.
        if all([char.value == " " for char in chars]):
            return self.render_chord_only(chords)

        # Initialize lists to work with because str are immutable.
        chord_line = [" "] * line_len
        lyric_line = [" "] * line_len
        pos = 0

        while chords:
            # Remove the first chord from the list of all chords.
            chord = chords.pop(0)

            # If the position is not where the chord starts, then it means one
            # of two things:
            # 1. We have not written enough of the lyrics line to be at the
            #    right position yet.
            # 2. We have written a chord whose position overlaps another chord.
            while pos != chord.start:

                # Case #2: when we start, if the next chord's start is already
                # less than the current position, it means we overlapped chords.
                if pos > chord.start:
                    # To fix this, we figure out how far ahead the position is
                    # and compute an offset between the two. This offset is
                    # used to increase the position of the chord, AND every
                    # token, both chord or char, ahead of it.
                    offset = pos - chord.start
                    chord.start += offset
                    chord.end += offset
                    for i in range(0, len(chords)):
                        chords[i].start += offset
                        chords[i].end += offset
                    for i in range(0, len(chars)):
                        chars[i].start += offset
                        chars[i].end += offset
                    # The reason we do this is because in order to rectify this
                    # we basically need to insert spaces. Since the lists
                    # already have spaces, advancing positions like this is
                    # functionally the same.
                
                # Case #1: The chord's position is ahead of the current position.
                # Here, we want to both add spaces to the chords line, and add
                # chars to the lyrics line.
                else:
                    chord_line[pos] = " "
                    try:
                        char = chars.pop(0).value
                    except IndexError:
                        # Well, while we can anyway. If an IndexError happens
                        # here, it means there's no more characters. If this
                        # happens, we just append spaces.
                        char = " "

                    lyric_line[pos] = char
                    pos += 1
            
            # We are now at a point where we're at the position of the next
            # chord in the list.
            for cchar in chord.value:
                # So we'll start by appending each char of the chord to the
                # chord line.
                try:
                    chord_line[pos] = cchar
                except IndexError:
                    # If an IndexError occurs here, it means we ran out of
                    # space on the chord line, but there's still characters
                    # left to append. So we'll append a space to the lyrics
                    # line, and append the chord's char instead over ovewriting.
                    chord_line.append(cchar)
                    lyric_line.append(" ")

                # After appending the chord's char, we do the same for lyrics.
                try:
                    char = chars.pop(0).value
                except IndexError:
                    char = " "
                lyric_line[pos] = char
                pos += 1
        
        # At this point, we've exhausted all chords. If there are remaining
        # lyrics, we can go through the rest.
        while chars:
            lyric_line[pos] = chars.pop(0).value
            pos += 1
        
        line = f"{''.join(chord_line)}\n{''.join(lyric_line)}\n"
        return line
    
    def __repr__(self) -> str:
        return self.render()


class Renderer:
    """
    The renderer class
    
    Renderer objects are initialized with a list of Section tokens
    from Hibiki's lexer. Calling Renderer.render() then causes
    the tokens to be rendered into their correct format and returned
    as a str.

    Attributes
    ----------
    tokens : t.List[Section] | The section tokens from the lexer.
    section_delimiter : str  | Each section will be separated by this str.
    """
    def __init__(self, tokens: t.List[Section]):
        self.tokens = tokens
        self.section_delimiter: str = "\n\n"
    
    def render(self):
        # Initialize an empty list to hold sections.
        sections = []

        for section in self.tokens:
            text = ""

            # Render the header first
            text += section.header.render()

            lines: t.List[Line] = []
            line_tokens: t.List[Token] = []

            # Then split the section's tokens up into lines.
            for token in section.tokens:
                if isinstance(token, NewLine):
                    lines.append(Line(line_tokens))
                    line_tokens = []
                else:
                    line_tokens.append(token)
            
            # Finally, for each line, render it.
            for line in lines:
                text += line.render()
            sections.append(text)
        
        # Join rendered sections together with the delimiter.
        return self.section_delimiter.join(sections)

            