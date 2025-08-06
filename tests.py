from hibiki.stanza import Line, Stanza
from hibiki.tab import Tab


class TestLine:
    inpt1 = "{A}Test{B}ing is {Cadd9}go{Am}od"
    inpt2 = "{A}  test {Cadd9}spa{Bbadd9}cing"

    def test_chord_output(self):
        otpt = "A   B      Cadd9 Am"
        
        line = Line(None, self.inpt1, 1)
        assert line.render_split()[0] == otpt
    
    def test_lyric_output(self):
        otpt = "Testing is go    od"
        line = Line(None, self.inpt1, 1)
        assert line.render_split()[1] == otpt
    
    def test_chord_spacing(self):
        chord_opt = "A      Cadd9 Bbadd9"
        lyric_opt = "  test spa   cing"

        line = Line(None, self.inpt2, 1)
        chords, lyrics = line.render_split()
        assert chords == chord_opt
        assert lyrics == lyric_opt


class TestChord:
    inpt1 = "{A|}chuck {B_}palm mute {(C)}sustained {NC}no chords {A7hA}hammer into"
    
    def test_modifiers(self):
        line = Line(None, self.inpt1, 1)

        chord_objs, lyrics = line.split_chords_and_lyrics()
        assert chord_objs[0].chucked == True # type: ignore
        assert chord_objs[1].palm_muted == True # type: ignore
        assert chord_objs[2].sustained == True # type: ignore
        assert chord_objs[3].non_chord == True # type: ignore
        assert chord_objs[4].hammer_into.symbol == "A" # type: ignore

        chord_opt = "A|    B_        (C)       N.C.      A7hA"
        lyric_opt = "chuck palm mute sustained no chords hammer into"
        chords, lyrics = line.render_split()
        assert chords == chord_opt
        assert lyrics == lyric_opt
    

class TestStanza:
    inpt = "[Verse 1]\n{C} Duplicate line (x3)\n\n"
     
    def test_name(self):
        stanza = Stanza(self.inpt, 1)
        assert stanza.name == "Verse 1"
    
    def test_duplication(self):
        stanza = Stanza(self.inpt, 1)
        assert len(stanza.lines) == 3


class TestTab:
    inpt = "{C} {A} {D}(#=prog1)\n\n[Verse 1]\nThis {C}is a {Am}song\nWith (@prog1)chords re{Am}called {A}\nWith (@prog1)chords re{Am}called {A}"

    def test_recall_len(self):
        tab = Tab(self.inpt)
        _ = tab.pre_process()
        assert len(tab._recalls) == 1
    
    def test_recall_val(self):
        tab = Tab(self.inpt)
        _ = tab.pre_process()
        assert tab._recalls['prog1'] == "{C} {A} {D}"

    def test_eq1(self):
        tab = Tab(self.inpt)
        out = tab.render(section_breaks=0).split("\n")
        assert out[4] == out[6]
    
    def test_eq2(self):
        tab = Tab(self.inpt)
        out = tab.render(section_breaks=0).split("\n")
        assert out[3] == out[5]
    
    def test_line_length(self):
        tab = Tab(self.inpt)
        assert len(tab.render(section_breaks=0).split("\n")) == 8