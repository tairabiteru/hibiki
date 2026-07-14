"""Integration tests combining multiple features."""

from hibiki import HibikiParser, HibikiRenderer


class TestComplexScenarios:
    """Tests for complex real-world scenarios."""

    def test_verse_chorus_song_structure(self):
        """Test typical verse-chorus song structure."""
        text = """[Verse 1]
In the morning sun

[Chorus]
We will rise again

[Verse 2]
In the evening light

[Chorus]

"""
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 4
        assert stanzas[0].name == "Verse 1"
        assert stanzas[1].name == "Chorus"
        assert stanzas[2].name == "Verse 2"
        assert stanzas[3].name == "Chorus"

    def test_song_with_chords_and_repeats(self):
        """Test song with both chords and repeats."""
        text = """[Verse]
{C}First line (x2)
{F}Second line

[Chorus] (x2)
{G}Chorus content

"""
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 3
        # Chorus repeated twice
        assert stanzas[1].name == "Chorus"
        assert stanzas[2].name == "Chorus"

    def test_complete_example_from_spec(self):
        """Test the complete example from SPEC.md."""
        text = """You can't see me here.(=phantom)

[Chorus]
The statement below is false:
(*phantom)

"""
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 1
        assert stanzas[0].name == "Chorus"
        assert "You can't see me here." in stanzas[0].lines[1].text

    def test_line_recall_across_multiple_stanzas(self):
        """Test recalling a line across multiple stanzas."""
        text = """Common refrain(=refrain)

[Verse 1]
First verse
(*refrain)

[Verse 2]
Second verse
(*refrain)

"""
        parser = HibikiParser()
        stanzas = parser.parse(text)
        assert len(stanzas) == 2
        assert "Common refrain" in stanzas[0].lines[1].text
        assert "Common refrain" in stanzas[1].lines[1].text


class TestIntegration:
    """Integration tests combining multiple features."""

    def test_full_workflow_parse_and_render(self):
        """Test complete workflow from parsing to rendering."""
        text = """[Verse 1]
{C}Hello world
This is line 2

[Chorus] (x2)
{F}Chorus line

"""
        parser = HibikiParser()
        stanzas = parser.parse(text)

        renderer = HibikiRenderer()
        output = renderer.render(stanzas)

        assert "[Verse 1]" in output
        assert "[Chorus]" in output
        assert "Hello world" in output
        assert "Chorus line" in output

    def test_parse_render_with_all_features(self):
        """Test rendering with chords, repeats, and recalls."""
        text = """Refrain line(=ref)

[Verse]
{C}Start line (x2)
{F}End with (*ref)

[Chorus]
{G}Chorus

[Verse]

"""
        parser = HibikiParser()
        stanzas = parser.parse(text)

        renderer = HibikiRenderer()
        output = renderer.render(stanzas)

        # Verify all elements are present
        assert output.count("[Verse]") == 2
        assert output.count("[Chorus]") == 1
        assert output.count("Start line") == 4
        assert output.endswith("End with Refrain line\n\n\n")
        assert output.count("Refrain line") == 2
