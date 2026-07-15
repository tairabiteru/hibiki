"""
Parser for the Hibiki Language.

Exposes both a `HibikiParser` class and a `parse` function for convenience.
"""

from __future__ import annotations
import re

from hibiki.errors import EmptyStanza, RedefinedStanza, UndefinedRecall, ChordSyntaxError
from .stanza import Stanza
from .lexer import hibiki_lexer


class HibikiParser:
    def __init__(self):
        self.stanzas: list[Stanza] = []
        self.current_heading: str | None = None
        self.current_stanza_text: str = ""
        self.current_stanza_line: int = 0
        self.current_repeat_count: int = 1
        self.line_num = 1
        self.recalls: dict[str, str] = {}


    def _finish_stanza(self) -> None:
        """Completes the existing stanza and adds it to the list."""
        if self.current_heading is None or not self.current_stanza_text.strip():
            return

        stanza = Stanza(self.current_heading, self.current_stanza_text, self.current_stanza_line, repeat_count=self.current_repeat_count)
        self.stanzas.append(stanza)


    def _preprocess_recalls(self, text: str) -> str:
        """
        Extract recall saves and substitute recall calls.

        Parameters
        ----------
        text: str
            The text to preprocess.

        Returns
        -------
        str
            The preprocessed text with recalls substituted.
        """
        lines = text.split('\n')
        out = []

        for i, line in enumerate(lines):
            # Check for recall save (=name)
            save_match = re.search(r'\(=\w+\)$', line)
            if save_match:
                var_name = save_match.group()[2:-1]  # Extract name from (=name)
                line_without_save = line[:save_match.start()]
                self.recalls[var_name] = line_without_save
                line = line_without_save

            # Check for recall recall (@name)
            for match in re.finditer(r'\(\*\w+\)', line):
                var_name = match.group()[2:-1]  # Extract name from (@name)
                if var_name in self.recalls:
                    line = line.replace(match.group(), self.recalls[var_name])
                else:
                    raise UndefinedRecall(i+1, var_name)

            out.append(line)

        return '\n'.join(out)

    def _preprocess(self, text: str) -> str:
        """
        Preprocesses the input text.

        Preprocessing is currently only used to handle recalls, but this
        function is defined anyway as an entry into the system for preprocessing.

        Parameters
        ----------
        text: str
            The text to preprocess.

        Returns
        -------
        str
            The preprocessed text.
        """
        text = self._preprocess_recalls(text)
        return text

    def _postprocess_heading_recalls(self, stanzas: list[Stanza]) -> list[Stanza]:
        """
        Postprocesses the stanzas to handle heading recalls.

        Parameters
        ----------
        stanzas: list[Stanza]
            The list of stanzas to postprocess.

        Returns
        -------
        list[Stanza]
            The postprocessed list of stanzas.
        """
        # Dictionary to save stanzas by heading
        saved = {}

        # Iterate through stanzas and save empty ones by heading
        for i, stanza in enumerate(stanzas):
            if stanza.is_empty:
                try:
                    saved_stanza = saved[stanza.heading]
                    stanzas[i] = Stanza(saved_stanza.heading, saved_stanza.text, saved_stanza.starting_line, repeat_count=stanza.repeat_count)
                except KeyError:
                    # If we get here, it means no saved stanza was found for this heading.
                    raise EmptyStanza(stanza)
            else:
                existing = saved.get(stanza.heading, None)
                if existing is not None and existing is not stanza:
                    # If we get here, it means a saved stanza was found for this heading, but it's not the same stanza.
                    # This indicates a redefinition of the stanza, so we raise an error.
                    raise RedefinedStanza(stanza, existing)
                else:
                    saved[stanza.heading] = stanza
        return stanzas

    def _postprocess_heading_repeats(self, stanzas: list[Stanza]) -> list[Stanza]:
        """
        Postprocesses the stanza list by repeating stanzas based on their repeat count.

        Parameters
        ----------
        stanzas: list[Stanza]
            The list of stanzas to postprocess.

        Returns
        -------
        list[Stanza]
            The postprocessed list of stanzas.
        """
        # Buffer to hold the postprocessed stanzas
        out = []

        # Repeat each stanza based on its repeat count
        for stanza in stanzas:
            out.append(stanza)
            # Repeat the stanza if its repeat count is greater than 1
            if stanza.repeat_count > 1:
                # Append the stanza to the output buffer for each repeat
                for _ in range(stanza.repeat_count-1):
                    out.append(stanza)
        return out

    def _postprocess(self, stanzas: list[Stanza]) -> list[Stanza]:
        """
        Postprocesses the stanza list.

        Postprocessing is handles heading recalls and repeats.
        This function exists as an entry point for postprocessing.

        Parameters
        ----------
        stanzas: list[Stanza]
            The stanzas to postprocess.

        Returns
        -------
        list[Stanza]
            The postprocessed stanzas.
        """
        stanzas = self._postprocess_heading_recalls(stanzas)
        stanzas = self._postprocess_heading_repeats(stanzas)
        return stanzas

    def parse(self, text: str) -> list[Stanza]:
        """
        Parse Hibiki source code into Stanza objects.

        Parameters
        ----------
        text: str
            The Hibiki source code to parse.

        Returns
        -------
        list[Stanza]
            A list of parsed Stanza objects.
        """
        # Hibiki files need to end with a newline.
        if not text.endswith("\n\n"):
            text += "\n\n"

        # Preprocess to extract and handle recalls
        text = self._preprocess(text)

        # Tokenize the input
        hibiki_lexer.input(text)

        # Process tokens
        try:
            while True:
                tok = hibiki_lexer.token()
                if not tok:
                    break

                if tok.type == 'HEADING':
                    # Finish previous stanza if it exists
                    if self.current_heading is not None:
                        self._finish_stanza()

                    # Start new stanza
                    heading, repeat_count = tok.value
                    self.current_heading = heading
                    self.current_repeat_count = repeat_count
                    self.current_stanza_text = f"[{heading}]\n"
                    self.current_stanza_line = self.line_num

                elif tok.type == 'NEWLINE':
                    # Handle line breaks
                    num_breaks = len(tok.value)
                    for _ in range(num_breaks):
                        if self.current_heading is not None:
                            self.current_stanza_text += "\n"
                            # Double newline ends a stanza
                            if self.current_stanza_text.endswith("\n\n"):
                                self._finish_stanza()
                                self.current_heading = None
                                self.current_stanza_text = ""
                    self.line_num += num_breaks

                elif tok.type == 'CHORD':
                    # Add chord with braces restored
                    if self.current_heading is not None:
                        self.current_stanza_text += f"{{{tok.value}}}"
                    self.line_num += 1

                else:
                    # Add other token content (FRAGMENT)
                    if self.current_heading is not None:
                        self.current_stanza_text += tok.value
                    self.line_num += 1
        except SyntaxError as e:
            # Convert chord-related syntax errors to ChordSyntaxError
            if '{' in str(e) or '}' in str(e):
                stanza_name = self.current_heading or "unknown"
                raise ChordSyntaxError(line_num=self.line_num, stanza_name=stanza_name, reason=str(e))
            raise

        # Finish any remaining stanza
        if self.current_heading is not None:
            self._finish_stanza()

        self.stanzas = self._postprocess(self.stanzas)
        return self.stanzas


def parse(text: str) -> list[Stanza]:
    """
    Shortcut to parsing Hibiki source code.

    Transforms Hibiki source code into a list of Stanza objects.

    Parameters
    ----------
    text: str
        The Hibiki source code to parse.

    Returns
    -------
    list[Stanza]
        A list of parsed Stanza objects.
    """
    return HibikiParser().parse(text)
