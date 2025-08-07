from __future__ import annotations
import re
import typing as t

from .stanza import Stanza
from .errors import EmptyStanza, RedefinedStanza, StanzaSyntaxError
from .utils import replace_all


class Tab:
    """
    A piece of musical tablature.

    Attributes
    ----------
    text: str
        The text making up the tablature.
    """
    FILLED_SECTION_REGEX = r"\[.+\]\n(.+\n)+"
    EMPTY_SECTION_REGEX = r"\[.+\]\n{2}"
    HEADER_REGEX = r"\[.+\]\n"
    RECALL_SAVE_REGEX = r"\(=\w+\)$"
    RECALL_OUT_REGEX = r"\(@\w+\)"

    def __init__(self, text: str):
        self.text = text
        self._recalls = {}

        # Hibiki tabs must end with two newlines.
        if not self.text.endswith("\n\n"):
            self.text += "\n\n"
    
    def pre_process(self) -> t.List[str]:
        """
        Pre-processor
        
        This function effectively alters the text in-situ before rendering.
        Mainly used for recalls at the moment, but it could in theory be used
        for more in the future.
        """
        out = []
        for line in self.text.split("\n"):
            match: t.Match[str] | None = re.search(self.RECALL_SAVE_REGEX, line)

            if match:
                line = line.replace(match.group(), "")
                var_name: str = replace_all(match.group(), "(=#)\n", "")
                self._recalls[var_name] = line
            
            out.append(line)
        return out


    def get_stanzas(self) -> t.List[Stanza]:
        """Obtain a list of stanzas in the tablature."""
        # The line count across the whole tab sheet
        line_count = 1

        # The place where the last encountered header was.
        started_at = 1

        # Buffer to hold the current stanza's text
        current_stanza = ""

        # Flag denoting whether or not we're currently in a stanza.
        in_stanza = False

        # Buffer to append stanzas to.
        stanzas = []

        # Obtain lines from pre-processor
        for line in self.pre_process():
            # For recall matches.
            match = re.search(self.RECALL_OUT_REGEX, line)

            # If one exists, we substitute it out for the recalled line
            if match:
                var_name: str = replace_all(match.group(), "(@)\n", "")
                line = re.sub(self.RECALL_OUT_REGEX, self._recalls[var_name], line)

            if in_stanza is True:
                # If we're in a stanza, a line can't begin with a [, that's a syntax error.
                if line.startswith("["):
                    raise StanzaSyntaxError(line_count, "New stanza character found in existing stanza.")
                
                # If a line is empty, that means the stanza has ended. 
                # (\n\n when split yields "")
                elif line == "":
                    current_stanza += "\n"
                    in_stanza = False
                    stanza = Stanza(current_stanza, started_at)
                    stanzas.append(stanza)
                    current_stanza = ""
                
                # Otherwise, keep append to the current stanza's text.
                else:
                    current_stanza += f"{line}\n"
            else:
                # If we're not in a stanza and the line starts with a [,
                # then a new stanza is beginning.
                if line.startswith("["):
                    started_at = line_count
                    current_stanza += f"{line}\n"
                    in_stanza = True
            
            line_count += 1

        return stanzas
    
    def render(self, section_breaks: int=2) -> str:
        """
        Render a tab sheet.

        Parameters
        ----------
        section_breaks: int
            The number of line breaks between sections.
        """
        stanzas = self.get_stanzas()

        # Dict mapping stanza names to stanzas.
        previous = {}

        # Buffer to hold output.
        out = ""

        for stanza in stanzas:
            if stanza.is_empty is True:
                # If the stanza is empty, we check to see if it's been
                # previously defined.
                prev_stanza = previous.get(stanza.name)

                # If not, that's an error.
                if prev_stanza is None:
                    raise EmptyStanza(stanza)
                
                # Otherwise, carry on using the existing stanza.
                else:
                    stanza = prev_stanza
            
            else:
                # If the stanza isn't empty, check to see if one by that name
                # already exists.
                prev_stanza = previous.get(stanza.name)

                # If it does, that's an error.
                if prev_stanza is not None:
                    raise RedefinedStanza(stanza, prev_stanza)

            # Append stanza's name
            out += f"[{stanza.name}]\n"

            # Then render each line and append the output.
            for line in stanza.lines:
                out += line.render()
            
            # Finally, append the number of linebreaks requested.
            out += "\n" * section_breaks

            # If a stanza isn't empty, append it to the dict
            # so it can be referenced in the future.
            if stanza.is_empty is False:
                previous[stanza.name] = stanza

        return out
    
    @classmethod
    def from_path(cls, path: str) -> Tab:
        """
        Shortcut to load from a file rather than from text.

        Parameters
        ----------
        path: str
            A path to the final containing hibiki source.
        """
        with open(path, "r") as file:
            return cls(file.read())


    
