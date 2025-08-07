# 0.3.0
- Removed "phantom recalls". They can be done all the same as normal recalls by simply defining them outside of the body of a stanza.
- Added missing docstrings for `hibiki.Chord`.
- Added basic command line handling to pass in files.
# 0.2.1
- Added the `note` property to `Chord`. This contains only the note of the chord, not any modifiers.
# 0.2.0
- Introduced "recalls" which allows a line to be duplicated entirely at a different point in the song.
```
[Verse 1]
This is {C}my {Am}line (=my_line)

[Verse 2]
(@my_line)
```
```
[Verse 1]
        C  Am
This is my line

[Verse 2]
        C  Am
This is my line
```
- Introduced "phantom recalls" which allows a line to be referenced and duplicated, but whose definition will not be rendered.
```
{C} {Csus4} {C} {Csus2} {C}(#=progression)

[Verse 1]
My song (@progression) has chords
```
```
[Verse 1]
        C Csus4 C Csus 2 C
My song                   has chords
```
- Fixed a bug in rendering which could rarely appear when using long chord progressions together.
- Removed old regex functions from `hibiki/utils.py` as they're not needed anymore.
- Added this changelog.
# 0.1.0
- First version