import typing as t

if t.TYPE_CHECKING:
    from stanza import Stanza, Line

class HibikiError(Exception):
    """
    General error thrown by Hibiki.

    Attributes
    ----------
    message: str
        The message to be displayed by the error.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class EmptyStanza(HibikiError):
    """
    Thrown when an empty stanza exists without previous definition.

    Hibiki allows auto-duplication of stanzas when they have already been
    defined previously. However, this of course can only be done if a
    the stanza in question *has* been previously defined. If it hasn't,
    Hibiki throws this error.

    Attributes
    ----------
    stanza: Stanza
        The stanza with an empty body which caused this error.
    """
    def __init__(self, stanza: "Stanza"):
        self.stanza = stanza
        super().__init__(f"Line #{stanza.starting_line}: Stanza '{stanza.name}' not previously defined was defined without a body.")


class RedefinedStanza(HibikiError):
    """
    Thrown when a stanza is given a name that's already been used.

    Converse to an EmptyStanza error, this is thrown when you try to
    "overwrite" a previously named stanza. It occurs when, as an example,
    you define [Verse 1] with a body, and then go on to define *another*
    [Verse 1] later. Hibiki does not allow this.

    Attributes
    ----------
    stanza: Stanza
        The stanza which caused this error.
    existing_stanza: Stanza
        The previously defined stanza whose name matches.
    """
    def __init__(self, stanza: "Stanza", existing_stanza: "Stanza"):
        self.stanza = stanza
        self.existing_stanza = existing_stanza
        super().__init__(f"Line #{stanza.starting_line}: Stanza '{stanza.name}' has a body but was previously defined on line #{existing_stanza.starting_line}.")


class UndefinedRecall(HibikiError):
    def __init__(self, line_no: int, var_name: str):
        self.line_no = line_no
        self.var_name = var_name
        super().__init__(f"Line #{line_no}: Undefined recall variable '{var_name}'.")


class ChordSyntaxError(HibikiError):
    """
    This error is thrown when some syntax error occurs with a chord. This is
    primarily chords with unclosed {braces}.

    Attributes
    ----------
    line: Line | None
        The line where the syntax error can be found.
    reason: str
        The reason for the syntax error.
    line_num: int | None
        The line number (used when Line object is unavailable).
    stanza_name: str | None
        The stanza name (used when Line object is unavailable).
    """
    def __init__(self, line: "Line | None" = None, reason: str = "", line_num: int | None = None, stanza_name: str | None = None):
        self.line = line
        self.reason = reason

        if line is not None:
            message = f"Line #{line.line_num}, Syntax Error in '{line.stanza.name}': {reason}"
        else:
            message = f"Line #{line_num}, Syntax Error in '{stanza_name}': {reason}"

        super().__init__(message)


class StanzaSyntaxError(HibikiError):
    """
    Thrown when syntax error occurs with a stanza.

    Attributes
    ----------
    line_num: int
        The line where the syntax error can be found.
    reason: str
        The reason for the syntax error.
    """
    def __init__(self, line_num: int, reason: str):
        self.line_num = line_num
        self.reason = reason
        super().__init__(f"Line #{line_num}, Syntax Error in on line {self.line_num}: {reason}")
