import typing as t

class Chord:
    """
    A chord found within a Line.

    Important to note here is that Hibiki does NOT make a distinction between
    "real" and "fake" chords. From Hibiki's standpoint, {Q#m7} is a valid
    chord. Hibiki's job is not to determine whether or not chords are real or
    not. It is only to determine if a "chord" appears within brackets, and
    whether or not it has any "modifiers" attached to it.

    Attributes
    ----------
    text: str:
        The text comprising the chord.
    symbol: str:
        The symbol comprising the chord. This is distinct from the text as the
        it contains the original text, whereas the symbol can be modified by
        Hibiki's modifier system.
    note: str:
        The note's symbol (excluding modifiers)
    sustained: bool
        Whether or not the chord is a sustained chord.
    chucked: bool
        Whether or not the chord is a chucked chord.
    non_chord: bool
        Whether or not the chord is a non-chord.
    palm_muted: bool
        Whether or not the chord is a palm muted chord.
    hammer_into: t.Optional[Chord]
        A chord which this chord is hammered into. None if it's not a hammered
        chord.
    """
    def __init__(self, text: str):
        self.text: str = text
        self.symbol: str = text

        self.sustained: bool = False
        self.chucked: bool = False
        self.non_chord: bool = False
        self.palm_muted: bool = False
        self.hammer_into: t.Optional[Chord] = None

        self.apply_modifiers()
    
    def __repr__(self) -> str:
        return f"<Chord: {self.symbol}>"
    
    @property
    def note(self) -> str:
        if self.chucked or self.palm_muted:
            return self.symbol[:-1]
        elif self.sustained:
            return self.symbol[1:-1]
        elif self.non_chord:
            return "N.C."
        else:
            return self.symbol

    def apply_modifiers(self) -> None:
        """
        Apply modifiers.

        Here we're checking for different chord modifiers and applying
        properties based on them.
        """
        if self.text.startswith("(") and self.text.endswith(")"):
            self.sustained = True
            self.symbol = f"({self.text[1:-1]})"
        if self.text.endswith("|"):
            self.chucked = True
            self.symbol = f"{self.text[:-1]}|"
        if self.text.replace(".", "") == "NC":
            self.non_chord = True
            self.symbol = "N.C."
        if self.text.endswith("_"):
            self.palm_muted = True
            self.symbol = f"{self.text[:-1]}_"
        if "h" in self.text:
            pre, post = tuple(self.text.split("h"))
            self.hammer_into = Chord(post)
            self.symbol = f"{pre}h{self.hammer_into.symbol}"
        
    @property
    def tab_repr(self) -> str:
        """
        The tab representation of the chord.

        Once again, distinct from both the symbol and text as this not only
        contains modifiers, but also the space which prevents chords from being
        right next to each other.
        """
        return f"{self.symbol} "
    