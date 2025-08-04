import re
import typing as t


def reductive_regex_match(regex: str, text: str) -> t.Tuple[str, t.List[re.Match]]:
    """
    Reductively match and remove by regex.

    The basic idea behind this function is to find regex matches and then
    remove them from the string.
    """
    match = True
    matches = []

    while match:
        match = re.search(regex, text)

        if match:
            matches.append(match)
            text = text.replace(match.group(), "", count=1)
    
    return text, matches


def reductive_multi_regex_match(regexes: t.Iterable[str], text: str) -> t.List[t.Match[str]]:
    """
    Reductively match and remove by multiple regex expressions.

    Same thing as above really, except this function does so with multiple
    different regex patterns.
    """
    possible = [True]
    matches = []

    while any(possible):
        possible = []
        for regex in regexes:
            possible.append(re.search(regex, text))
        
        possible = list(filter(lambda x: x != None, possible))
        possible = sorted(possible, key=lambda x: x.span()[0])
        
        if any(possible):
            matches.append(possible[0])
            text = text.replace(possible[0].group(), "", count=1)

    return matches


def replace_all(
        text: str,
        matching_chars: t.Union[str, t.List[str]],
        replacing_char: str
    ) -> str:
    """
    Replace all instances of matching chars with replacing chars.
    """
    
    if not isinstance(matching_chars, list):
        matching_chars = list(matching_chars)
    
    for i in range(0, len(matching_chars)):
        text = text.replace(matching_chars[i], replacing_char)
    return text