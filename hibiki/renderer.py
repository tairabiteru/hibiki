from __future__ import annotations
from typing import overload

from .stanza import Stanza
from .parser import parse


class HibikiRenderer:
    """
    A renderer for Hibiki tablature.

    Renderers work to take a list of stanzas from the Hibiki parser and render them into a string.
    """
    def __init__(self, breaks_between_sections: int=2):
        self.breaks_between_sections = breaks_between_sections


    @overload
    def render(self, input: str) -> str:
        """
        Render a tab sheet from a raw tablature string.

        Parameters
        ----------
        input: str
            The raw tablature text to render.

        Returns
        -------
        str
            The rendered tab sheet.
        """
        ...

    @overload
    def render(self, input: list[Stanza]) -> str:
        """
        Render a tab sheet from a list of stanzas.

        Parameters
        ----------
        input: list[Stanza]
            The list of stanzas to render.

        Returns
        -------
        str
            The rendered tab sheet.
        """
        ...

    def render(self, input: str | list[Stanza]) -> str:
        """
        Render Hibiki source code into a tab sheet.

        Parameters
        ----------
        input: str | list[Stanza]
            The source code or list of stanzas to render.

        Returns
        -------
        str
            The rendered tab sheet.
        """
        if isinstance(input, str):
            stanzas = parse(input)
        else:
            stanzas = input

        output: str = ""

        for stanza in stanzas:
            output += f"[{stanza.name}]\n"
            for line in stanza.lines:
                output += line.render()
            output += "\n" * self.breaks_between_sections

        return output
