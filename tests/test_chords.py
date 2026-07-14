"""Tests for chord parsing, modifiers, and syntax error handling."""

import pytest
from hibiki import HibikiParser, HibikiRenderer, Chord
from hibiki.errors import ChordSyntaxError


class TestChords:
    """Tests for chord parsing and rendering."""

    def test_simple_chord(self):
        """Test parsing a simple chord."""
        text = "[Verse]\n{C}I'm a chord!\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 1
        line = stanzas[0].lines[0]
        chords, lyrics = line.split_chords_and_lyrics()
        assert len(chords) > 0
        assert isinstance(chords[0], Chord)
        assert chords[0].text == "C"

    def test_multiple_chords_on_line(self):
        """Test parsing multiple chords on a single line."""
        text = "[Verse]\n{Am}I'm a {C}chorus!\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        line = stanzas[0].lines[0]
        chords, lyrics = line.split_chords_and_lyrics()
        assert any(isinstance(c, Chord) for c in chords)

    def test_chord_with_complex_name(self):
        """Test that Hibiki accepts complex chord names."""
        text = "[Verse]\n{H#m7}Complex chord\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        line = stanzas[0].lines[0]
        chords, lyrics = line.split_chords_and_lyrics()
        assert any(c.text == "H#m7" for c in chords if isinstance(c, Chord))

    def test_chord_rendering_above_lyrics(self):
        """Test that chords are rendered above corresponding lyrics."""
        text = "[Verse]\n{C}Lyrics\n\n"
        renderer = HibikiRenderer()
        output = renderer.render(text)
        lines = output.split("\n")
        # Chord line should appear before lyric line
        chord_line = None
        lyric_line = None
        for i, line in enumerate(lines):
            if "C" in line and "Lyrics" not in line:
                chord_line = i
            if "Lyrics" in line:
                lyric_line = i
        assert chord_line is not None
        assert lyric_line is not None
        assert chord_line < lyric_line


class TestChordModifiers:
    """Tests for chord modifiers."""

    def test_sustained_chord(self):
        """Test sustained chord modifier (parentheses)."""
        chord = Chord("(C)")
        assert chord.sustained is True
        assert chord.symbol == "(C)"

    def test_chucked_chord(self):
        """Test chucked chord modifier (pipe)."""
        chord = Chord("C|")
        assert chord.chucked is True
        assert chord.symbol == "C|"

    def test_nc_chord(self):
        """Test N.C. (no chord) modifier."""
        chord = Chord("NC")
        assert chord.non_chord is True
        assert chord.symbol == "N.C."

    def test_palm_muted_chord(self):
        """Test palm muted chord modifier (underscore)."""
        chord = Chord("C_")
        assert chord.palm_muted is True
        assert chord.symbol == "C_"

    def test_hammer_into_chord(self):
        """Test hammer-on chord modifier."""
        chord = Chord("ChG")
        assert chord.hammer_into is not None
        assert chord.hammer_into.symbol == "G"


class TestChordSyntax:
    """Tests for chord syntax error handling."""

    def test_unclosed_chord_brace(self):
        """Test that unclosed chord brace raises ChordSyntaxError."""
        text = "[Verse]\n{C unclosed\n\n"
        parser = HibikiParser()
        with pytest.raises(ChordSyntaxError):
            parser.parse(text)

    def test_nested_chord_braces(self):
        """Test that nested chord braces raise ChordSyntaxError."""
        text = "[Verse]\n{C{inner}}\n\n"
        parser = HibikiParser()
        with pytest.raises(ChordSyntaxError):
            parser.parse(text)
