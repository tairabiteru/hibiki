"""Tests for stanza creation, parsing, and properties."""

import pytest
from hibiki import HibikiParser, EmptyStanza, RedefinedStanza


class TestStanzaBasics:
    """Tests for basic stanza creation and parsing."""

    def test_simple_stanza(self):
        """Test parsing a simple stanza."""
        text = "[Verse]\nHello world\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 1
        assert stanzas[0].name == "Verse"

    def test_stanza_with_multiple_lines(self):
        """Test stanza with multiple lines of text."""
        text = "[Chorus]\nLine 1\nLine 2\nLine 3\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 1
        assert stanzas[0].name == "Chorus"
        assert len(stanzas[0].lines) == 3

    def test_multiple_stanzas(self):
        """Test parsing multiple stanzas in sequence."""
        text = "[Verse 1]\nVerse content\n\n[Chorus]\nChorus content\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 2
        assert stanzas[0].name == "Verse 1"
        assert stanzas[1].name == "Chorus"

    def test_stanza_ending_with_double_newline(self):
        """Test that stanza ends with double newline."""
        text = "[Verse]\nContent\n\n[Chorus]\nMore content\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 2

    def test_text_outside_stanza_not_rendered(self):
        """Test that text outside stanzas is not rendered (phantom recall use case)."""
        text = "Outside text\n\n[Verse]\nInside text\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 1
        assert stanzas[0].name == "Verse"


class TestStanzaErrors:
    """Tests for stanza-related errors."""

    def test_redefined_stanza_with_body(self):
        """Test that redefining a stanza with a body raises RedefinedStanza."""
        text = "[Chorus]\nFirst chorus\n\n[Chorus]\nSecond chorus\n\n"
        parser = HibikiParser()
        with pytest.raises(RedefinedStanza):
            parser.parse(text)

    def test_empty_stanza_without_previous_definition(self):
        """Test that empty stanza without previous definition raises EmptyStanza."""
        text = "[Verse 1]\n\n"
        parser = HibikiParser()
        with pytest.raises(EmptyStanza):
            parser.parse(text)

    def test_valid_empty_stanza_with_previous_definition(self):
        """Test that empty stanza with previous definition is valid (stanza recall)."""
        text = "[Verse]\nContent\n\n[Verse]\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 2
        assert stanzas[0].name == "Verse"
        assert stanzas[1].name == "Verse"


class TestStanzaRecalls:
    """Tests for stanza recall functionality."""

    def test_simple_stanza_recall(self):
        """Test recalling a previously defined stanza."""
        text = "[Verse]\nVerse lyrics\n\n[Verse]\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 2
        # Both should have the same content
        assert stanzas[0].lines[0].text.strip() == stanzas[1].lines[0].text.strip()

    def test_multiple_stanza_recalls(self):
        """Test recalling the same stanza multiple times."""
        text = "[Chorus]\nChorus!\n\n[Chorus]\n\n[Chorus]\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 3

    def test_undefined_recall_raises_error(self):
        """Test that recalling an undefined stanza raises EmptyStanza."""
        text = "[Undefined]\n\n"
        parser = HibikiParser()
        with pytest.raises(EmptyStanza):
            parser.parse(text)


class TestStanzaProperties:
    """Tests for stanza properties."""

    def test_stanza_starting_line_number(self):
        """Test that stanza starting_line is recorded correctly."""
        text = "[Verse]\nContent\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert stanzas[0].starting_line == 1

    def test_stanza_is_empty_property(self):
        """Test the is_empty property of stanzas."""
        text = "[Verse]\n\n"
        parser = HibikiParser()
        with pytest.raises(EmptyStanza):
            parser.parse(text)

    def test_stanza_heading_property(self):
        """Test the heading property is stored correctly."""
        text = "[Test Heading]\nContent\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert stanzas[0].heading == "Test Heading"
