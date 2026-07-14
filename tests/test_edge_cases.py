"""Tests for edge cases and boundary conditions."""

from hibiki import HibikiParser, Chord


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_stanza_with_empty_lines(self):
        """Test stanza with empty lines within its body."""
        text = "[Verse]\nLine 1\n\nLine 2\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        # Empty line in middle ends stanza
        assert len(stanzas) == 1
        assert len(stanzas[0].lines) == 1

    def test_stanza_heading_with_special_characters(self):
        """Test stanza heading with numbers and spaces."""
        text = "[Verse 1 - Intro]\nContent\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert stanzas[0].name == "Verse 1 - Intro"

    def test_very_long_line_with_chords(self):
        """Test handling of very long lines with multiple chords."""
        text = "[Verse]\n{C}One {D}Two {E}Three {F}Four {G}Five\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        line = stanzas[0].lines[0]
        chords, lyrics = line.split_chords_and_lyrics()
        assert len([c for c in chords if isinstance(c, Chord)]) >= 5

    def test_line_starting_with_chord(self):
        """Test line that starts with a chord."""
        text = "[Verse]\n{C}Starting with chord\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        line = stanzas[0].lines[0]
        chords, lyrics = line.split_chords_and_lyrics()
        assert len(chords) > 0

    def test_line_ending_with_chord(self):
        """Test line that ends with a chord."""
        text = "[Verse]\nEnding with {C}\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        line = stanzas[0].lines[0]
        chords, lyrics = line.split_chords_and_lyrics()
        # Should handle the ending chord correctly
        assert len(lyrics) == len(chords)

    def test_stanza_with_only_chords(self):
        """Test stanza line with only chords (no lyrics)."""
        text = "[Verse]\n{C}{F}{G}\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        line = stanzas[0].lines[0]
        chords, lyrics = line.split_chords_and_lyrics()
        assert len(chords) >= 3
