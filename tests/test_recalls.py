"""Tests for line recalls and phantom recalls."""

import pytest
from hibiki import HibikiParser, HibikiRenderer, UndefinedRecall


class TestLineRecalls:
    """Tests for line recall functionality using (=name) and (*name)."""

    def test_simple_line_save_and_recall(self):
        """Test saving and recalling a line within a stanza."""
        text = "[Verse]\nI'm a verse(=var)\nRemember me? (*var)\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 1
        assert "I'm a verse" in stanzas[0].lines[0].text
        assert "I'm a verse" in stanzas[0].lines[1].text

    def test_line_recall_with_different_variable_names(self):
        """Test saving and recalling with different variable names."""
        text = "[Verse]\nLine 1(=first)\nLine 2(=second)\nRecall: (*first) and (*second)\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 1
        assert len(stanzas[0].lines) == 3
        assert "Line 1" in stanzas[0].lines[2].text
        assert "Line 2" in stanzas[0].lines[2].text

    def test_undefined_line_recall_raises_error(self):
        """Test that recalling an undefined variable raises UndefinedRecall."""
        text = "[Verse]\nSome text (*undefined_var)\n\n"
        parser = HibikiParser()
        with pytest.raises(UndefinedRecall):
            parser.parse(text)

    def test_valid_variable_names(self):
        """Test that variable names can contain letters, numbers, and underscores."""
        text = "[Verse]\nText(=var_123)\nRecall: (*var_123)\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 1
        assert "Text" in stanzas[0].lines[1].text


class TestPhantomRecall:
    """Tests for phantom recall (line save outside stanza)."""

    def test_phantom_recall_saves_line_outside_stanza(self):
        """Test that line saves outside stanzas don't appear in output."""
        text = "You can't see me(=phantom)\n\n[Chorus]\nRecall: (*phantom)\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 1
        assert stanzas[0].name == "Chorus"
        assert "You can't see me" in stanzas[0].lines[0].text

    def test_phantom_recall_in_rendered_output(self):
        """Test phantom recall appears correctly in rendered output."""
        text = "Hidden text(=hidden)\n\n[Verse]\nVisible: (*hidden)\n\n"
        renderer = HibikiRenderer()
        output = renderer.render(text)
        assert "Hidden text" in output
        assert "[Verse]" in output


class TestParserRecallHandling:
    """Tests for the parser's recall preprocessing."""

    def test_multiple_line_saves(self):
        """Test saving multiple lines with different variable names."""
        text = """Line A(=a)
Line B(=b)

[Verse]
Text with (*a) and (*b)

"""
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert "Line A" in stanzas[0].lines[0].text
        assert "Line B" in stanzas[0].lines[0].text

    def test_recall_overwriting(self):
        """Test that later saves overwrite earlier ones."""
        text = """Text 1(=var)
Text 2(=var)

[Verse]
Recall: (*var)

"""
        parser = HibikiParser()
        stanzas = parser.parse(text)
        # Should use the latest definition
        assert "Text 2" in stanzas[0].lines[0].text
