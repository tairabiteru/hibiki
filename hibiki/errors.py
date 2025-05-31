class DefinitionError(Exception):
    """
    Defines custom exception for a DefinitionError
    
    Definition errors occur when Hibiki detects a conflict in the naming
    of section definitions. Sections, (analogous to musical sections, like a
    chorus, verse, intro, etc...) are treated almost as constants in Hibiki,
    meaning they cannot be redefined. Attempting to redefine a section would
    result in a DefinitionError. For example:

    [Chorus]
    Some chorus with {C}a few {F}chords

    (later)

    [Chorus]
    The same chorus but with {F}different {C}contents.

    The second [Chorus] would cause a DefinitionError because
    [Chorus] has already been defined in the context of the song.
    Some songs have more than one chorus, but in that case, Hibiki
    mandates the use of something like [Chorus 1] and [Chorus 2].

    Another example of this is when you reference an undefined section.
    Hibiki allows you to skip typing an entire section of a song
    if it is a reprisal of a previous section:
    
    [Chorus]
    I am a {D}chorus!

    [Chorus]

    In the above, both sections would be rendered as if the first
    [Chorus]'s body was typed twice. However, you cannot do this
    of course if [Chorus] has not been defined first. If you try,
    a DefinitionError is also raised.
    """
    pass