"""Tests for line and stanza repeats using (xn) syntax."""

from hibiki import HibikiParser


class TestRepeats:
    """Tests for line and stanza repeats using (xn) syntax."""

    def test_line_repeat_x2(self):
        """Test repeating a line twice."""
        text = "[Verse]\nRepeat me! (x2)\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas[0].lines) == 2

    def test_line_repeat_x3(self):
        """Test repeating a line three times."""
        text = "[Verse]\nRepeat me! (x3)\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas[0].lines) == 3

    def test_stanza_repeat_x2(self):
        """Test repeating an entire stanza."""
        text = "[Chorus] (x2)\nChorus content\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 2

    def test_stanza_repeat_does_not_carry_across_recalls(self):
        """Test that stanza repeats don't carry across recalls."""
        text = "[Chorus] (x2)\nChorus content\n\n[Chorus]\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        # First stanza definition appears twice due to (x2)
        # Then a recall appears once
        assert len(stanzas) == 3
        # The recall should only appear once, not repeated
        assert stanzas[2].repeat_count == 1

    def test_multiple_lines_with_different_repeats(self):
        """Test multiple lines with different repeat counts."""
        text = "[Verse]\nLine 1 (x2)\nLine 2 (x3)\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        # Line 1 appears twice, Line 2 appears three times = 5 total
        assert len(stanzas[0].lines) == 5
