"""Tests for line number accuracy in error reporting and parsed stanzas."""

import pytest
from hibiki import HibikiParser
from hibiki.errors import (
    ChordSyntaxError,
    EmptyStanza,
    RedefinedStanza,
    UndefinedRecall,
)


class TestChordSyntaxErrorLineNumbers:
    """Tests that ChordSyntaxError reports correct line numbers."""

    def test_unclosed_chord_on_line_2(self):
        """Test unclosed chord error on line 2."""
        text = "[Verse]\n{C unclosed\n\n"
        parser = HibikiParser()
        with pytest.raises(ChordSyntaxError) as exc_info:
            parser.parse(text)
        assert "Line #2" in str(exc_info.value)

    def test_unclosed_chord_on_line_5(self):
        """Test unclosed chord error on line 5."""
        text = "[Verse]\nLine one\nLine two\nLine three\n{Am unclosed\n\n"
        parser = HibikiParser()
        with pytest.raises(ChordSyntaxError) as exc_info:
            parser.parse(text)
        assert "Line #5" in str(exc_info.value)

    def test_unclosed_chord_on_line_10(self):
        """Test unclosed chord error on line 10."""
        text = "[Verse]\n" + "Content\n" * 8 + "{G unclosed\n\n"
        parser = HibikiParser()
        with pytest.raises(ChordSyntaxError) as exc_info:
            parser.parse(text)
        assert "Line #10" in str(exc_info.value)

    def test_nested_chord_braces_on_line_3(self):
        """Test nested chord braces error on line 3."""
        text = "[Verse]\nSome content\n{C{inner}}\n\n"
        parser = HibikiParser()
        with pytest.raises(ChordSyntaxError) as exc_info:
            parser.parse(text)
        assert "Line #3" in str(exc_info.value)

    def test_invalid_chord_closing_on_line_4(self):
        """Test invalid chord closing brace on line 4."""
        text = "[Verse]\nLine 1\nLine 2\nInvalid } closing\n\n"
        parser = HibikiParser()
        with pytest.raises(ChordSyntaxError) as exc_info:
            parser.parse(text)
        assert "Line #4" in str(exc_info.value)


class TestEmptyStanzaErrorLineNumbers:
    """Tests that EmptyStanza error reports correct line numbers."""

    def test_empty_stanza_on_line_4(self):
        """Test empty stanza error on line 4."""
        text = "[Verse]\nContent\n\n[Chorus]\n\n"
        parser = HibikiParser()
        with pytest.raises(EmptyStanza) as exc_info:
            parser.parse(text)
        assert "Line #4" in str(exc_info.value)

    def test_empty_stanza_on_line_7(self):
        """Test empty stanza error on line 7."""
        text = "[Verse 1]\nContent\n\n[Verse 2]\nMore content\n\n[Verse 3]\n\n"
        parser = HibikiParser()
        with pytest.raises(EmptyStanza) as exc_info:
            parser.parse(text)
        assert "Line #7" in str(exc_info.value)

    def test_empty_stanza_after_blank_line_on_line_10(self):
        """Test empty stanza on line 10 with blank lines before it."""
        text = "[Verse]\nContent\n\n[Bridge]\nMore\n\n[Chorus]\nChorus content\n\n[Outro]\n\n"
        parser = HibikiParser()
        with pytest.raises(EmptyStanza) as exc_info:
            parser.parse(text)
        assert "Line #10" in str(exc_info.value)


class TestRedefinedStanzaErrorLineNumbers:
    """Tests that RedefinedStanza error reports correct line numbers."""

    def test_redefined_stanza_on_line_4(self):
        """Test redefined stanza error on line 4."""
        text = "[Verse]\nFirst definition\n\n[Verse]\nSecond definition\n\n"
        parser = HibikiParser()
        with pytest.raises(RedefinedStanza) as exc_info:
            parser.parse(text)
        assert "Line #4" in str(exc_info.value)

    def test_redefined_stanza_on_line_7(self):
        """Test redefined stanza error on line 7."""
        text = "[Verse]\nFirst\n\n[Chorus]\nChorus\n\n[Verse]\nSecond\n\n"
        parser = HibikiParser()
        with pytest.raises(RedefinedStanza) as exc_info:
            parser.parse(text)
        assert "Line #7" in str(exc_info.value)

    def test_redefined_stanza_with_complex_structure(self):
        """Test redefined stanza in more complex file."""
        text = (
            "[Intro]\nIntro content\n\n"
            "[Verse 1]\nVerse content\n\n"
            "[Chorus]\nChorus 1\n\n"
            "[Verse 2]\nMore verse\n\n"
            "[Chorus]\nChorus 2\n\n"
        )
        parser = HibikiParser()
        with pytest.raises(RedefinedStanza) as exc_info:
            parser.parse(text)
        # Second [Chorus] is on line 13
        assert "Line #13" in str(exc_info.value)


class TestUndefinedRecallErrorLineNumbers:
    """Tests that UndefinedRecall error reports correct line numbers."""

    def test_undefined_recall_on_line_2(self):
        """Test undefined recall error on line 2."""
        text = "[Verse]\nThis uses (*undefined)\n\n"
        parser = HibikiParser()
        with pytest.raises(UndefinedRecall) as exc_info:
            parser.parse(text)
        assert "Line #2" in str(exc_info.value)

    def test_undefined_recall_on_line_4(self):
        """Test undefined recall error on line 4."""
        text = "[Verse]\nLine 1\nLine 2\nUsing (*missing)\n\n"
        parser = HibikiParser()
        with pytest.raises(UndefinedRecall) as exc_info:
            parser.parse(text)
        assert "Line #4" in str(exc_info.value)

    def test_undefined_recall_on_line_6(self):
        """Test undefined recall error on line 6."""
        text = "[Verse]\nContent\n\n[Chorus]\nUsing (*never_defined)\n\n"
        parser = HibikiParser()
        with pytest.raises(UndefinedRecall) as exc_info:
            parser.parse(text)
        # Line 5 is where the undefined recall is
        assert "Line #5" in str(exc_info.value)


class TestParsedStanzaLineNumbers:
    """Tests that parsed stanzas have correct line numbers."""

    def test_simple_stanza_lines(self):
        """Test line numbers in a simple stanza."""
        text = "[Verse]\nLine 1\nLine 2\nLine 3\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert stanzas[0].starting_line == 1
        assert stanzas[0].lines[0].line_num == 2
        assert stanzas[0].lines[1].line_num == 3
        assert stanzas[0].lines[2].line_num == 4

    def test_multiple_stanzas_line_numbers(self):
        """Test line numbers across multiple stanzas."""
        text = (
            "[Verse 1]\n"
            "Line A\n"
            "Line B\n"
            "\n"
            "[Verse 2]\n"
            "Line C\n"
            "Line D\n"
            "\n"
        )
        parser = HibikiParser()
        stanzas = parser.parse(text)

        # Verse 1 on line 1
        assert stanzas[0].starting_line == 1
        assert stanzas[0].lines[0].line_num == 2
        assert stanzas[0].lines[1].line_num == 3

        # Verse 2 on line 5
        assert stanzas[1].starting_line == 5
        assert stanzas[1].lines[0].line_num == 6
        assert stanzas[1].lines[1].line_num == 7

    def test_stanzas_with_chords_line_numbers(self):
        """Test line numbers are correct even with chords on same line."""
        text = (
            "[Verse]\n"
            "Line {C}one {G}here\n"
            "Line {Am}two {Dm}here\n"
            "Line three\n"
            "\n"
        )
        parser = HibikiParser()
        stanzas = parser.parse(text)

        assert stanzas[0].starting_line == 1
        assert stanzas[0].lines[0].line_num == 2
        assert stanzas[0].lines[1].line_num == 3
        assert stanzas[0].lines[2].line_num == 4

    def test_stanzas_with_blank_lines_between_heading(self):
        """Test line numbers with blank lines between stanza headings."""
        text = (
            "[Verse 1]\n"
            "Content\n"
            "\n"
            "[Interlude]\n"
            "Interlude content\n"
            "\n"
            "[Verse 2]\n"
            "More content\n"
            "\n"
        )
        parser = HibikiParser()
        stanzas = parser.parse(text)

        # Verse 1 on line 1
        assert stanzas[0].starting_line == 1

        # Interlude on line 4
        assert stanzas[1].starting_line == 4

        # Verse 2 on line 7
        assert stanzas[2].starting_line == 7

    def test_complex_file_line_numbers(self):
        """Test line numbers in a complex file structure."""
        text = (
            "[Intro]\n"
            "{G} {D}\n"
            "\n"
            "[Verse 1]\n"
            "This is the first verse\n"
            "With multiple lines\n"
            "\n"
            "[Chorus]\n"
            "Chorus content here\n"
            "\n"
            "[Verse 2]\n"
            "Second verse\n"
            "\n"
        )
        parser = HibikiParser()
        stanzas = parser.parse(text)

        # Verify each stanza's starting line
        assert stanzas[0].starting_line == 1  # [Intro]
        assert stanzas[1].starting_line == 4  # [Verse 1]
        assert stanzas[2].starting_line == 8  # [Chorus]
        assert stanzas[3].starting_line == 11  # [Verse 2]

        # Verify line numbers within stanzas
        assert stanzas[1].lines[0].line_num == 5
        assert stanzas[1].lines[1].line_num == 6
        assert stanzas[2].lines[0].line_num == 9
        assert stanzas[3].lines[0].line_num == 12

    def test_stanza_with_repeats_line_numbers(self):
        """Test that stanzas with repeats have correct line numbers."""
        text = "[Verse]\nLine {C}one\nLine {D}two (x2)\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)

        # Starting line should be correct
        assert stanzas[0].starting_line == 1
        # Lines should have correct numbers
        assert stanzas[0].lines[0].line_num == 2
        # Second line appears twice due to (x2) but both instances have same line_num
        assert stanzas[0].lines[1].line_num == 3
        assert stanzas[0].lines[2].line_num == 3
