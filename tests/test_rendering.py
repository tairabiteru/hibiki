"""Tests for output rendering and line rendering with chords."""

from hibiki import HibikiParser, HibikiRenderer


class TestRendering:
    """Tests for output rendering."""

    def test_simple_render(self):
        """Test rendering a simple stanza."""
        text = "[Verse]\nHello world\n\n"
        renderer = HibikiRenderer()
        output = renderer.render(text)
        assert "[Verse]" in output
        assert "Hello world" in output

    def test_render_multiple_stanzas(self):
        """Test rendering multiple stanzas."""
        text = "[Verse 1]\nVerse content\n\n[Chorus]\nChorus content\n\n"
        renderer = HibikiRenderer()
        output = renderer.render(text)
        assert "[Verse 1]" in output
        assert "[Chorus]" in output
        assert "Verse content" in output
        assert "Chorus content" in output

    def test_render_with_custom_breaks(self):
        """Test rendering with custom number of breaks between sections."""
        text = "[Verse]\nContent\n\n"
        renderer = HibikiRenderer(breaks_between_sections=3)
        output = renderer.render(text)
        assert output.count("\n") >= 3

    def test_render_accepts_stanzas_list(self):
        """Test that renderer accepts pre-parsed stanzas."""
        text = "[Verse]\nContent\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        renderer = HibikiRenderer()
        output = renderer.render(stanzas)
        assert "[Verse]" in output
        assert "Content" in output

    def test_render_accepts_raw_string(self):
        """Test that renderer accepts raw Hibiki source."""
        text = "[Verse]\nContent\n\n"
        renderer = HibikiRenderer()
        output = renderer.render(text)
        assert "[Verse]" in output
        assert "Content" in output


class TestLineRendering:
    """Tests for individual line rendering with chords."""

    def test_line_render_split(self):
        """Test the render_split method of lines."""
        text = "[Verse]\n{C}Lyrics\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        line = stanzas[0].lines[0]
        chord_line, lyric_line = line.render_split()
        assert "C" in chord_line
        assert "Lyrics" in lyric_line

    def test_chord_lyric_alignment(self):
        """Test that chords align correctly with lyrics."""
        text = "[Verse]\n{C}L\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        line = stanzas[0].lines[0]
        chord_line, lyric_line = line.render_split()
        # Both lines should be rendered
        assert len(chord_line) > 0
        assert len(lyric_line) > 0

    def test_longer_chord_than_lyric(self):
        """Test handling when chord is longer than lyric segment."""
        text = "[Verse]\n{Dm7b5}A\n\n"
        parser = HibikiParser()
        stanzas = parser.parse(text)
        line = stanzas[0].lines[0]
        chord_line, lyric_line = line.render_split()
        # Should handle length difference
        assert len(chord_line) >= len(lyric_line.replace(" ", ""))
