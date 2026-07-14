"""
Lexer for the Hibiki Language.

Lexer is based on PLY (Python Lex-Yacc) and tokenizes via regular expressions.
"""
from __future__ import annotations
import re

import ply.lex as lex


tokens = (
    'HEADING',
    'CHORD',
    'FRAGMENT',
    'NEWLINE',
)


# The heading of a stanza
def t_HEADING(t):
    r'\[[^\]]+\](?:\s*\(\s*x\s*\d+\s*\))?\s*\n'

    raw = t.value.strip('\n').strip()

    # Extract repeat count if present (e.g., "(x2)")
    repeat_match = re.search(r'\(\s*x\s*(\d+)\s*\)', raw)
    if repeat_match:
        repeat_count = int(repeat_match.group(1))
        heading = raw[:repeat_match.start()].strip().strip('[]')
    else:
        repeat_count = 1
        heading = raw.strip('[]').strip()

    t.value = (heading, repeat_count)
    t.name = heading.replace("[", "").replace("]", "").strip()
    t.lexer.lineno += 1
    return t

# Chords, ex {Cm}, {Bb}, {F#m}, etc...
def t_CHORD(t):
    r'\{[^}]+\}'
    t.value = t.value[1:-1]  # Strip braces
    return t

# Fragments belonging to a chord.
def t_FRAGMENT(t):
    r'[^{}\[\]\n]+'
    return t

## Newline characters
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lineno}")


hibiki_lexer = lex.lex()
