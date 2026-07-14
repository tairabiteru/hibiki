# Hibiki Language Specification
Hibiki is a markup language made to write musical tabs. This file acts as a "white paper" of sorts for Hibiki, describing formally what the language is, and how its syntax is defined at a high level. This can be used both as documentation for the language as well as a source of truth defining what is correct behavior, and what is not.

## File Format
Hibiki files shall have the extensions `.hb` on them. `.hb` files will be plain text files containing Hibiki source code.

## Stanzas
A stanza is essentially a section of a song. For Hibiki, the beginning of a stanza is marked by an opening bracket `[`, followed by any text including spaces, followed by a closing bracket `]` and a newline character. A stanza is then ended when two newline characters are found right next to each other after the start of a stanza. This in practice looks like this:
```
1 [Chorus]
2 Hi, I'm a chorus!
3 
4 
5 Some other text.
```
The heading `[Chorus]` indicates the start of a new stanza at the end of line 1. Line 2 and 3 comprise the body of the stanza, but on line 4 we're no longer in the stanza, as there's a newline character at the end of line 2 and then one immediately after on line 3, ending the current stanza.

An important note is that all text to be rendered in Hibiki __must__ appear in a stanza. In the example above, the text on line 5 will not throw an error, but it also will not be rendered. This can be useful for making comments, but also for performing "phantom recalls". (Explained later.) Each newly defined stanza's heading must have a __unique name__. If there are two different choruses in a song, each must be named differently. (Ex, [Chorus 1] and [Chorus 2]). The following shows an invalid Hibiki file:
```
1 [Chorus]
2 I'm a chorus!
3 
4 [Chorus]
5 I'm also a chorus!
6 
```
Hibiki will throw a `RedefinedStanza` error in this situation, because the stanza on line 1 is named `Chorus` and has a body defined, but there is another stanza with the same name on line 4 which also has a body defined. This is not allowed.

# Stanza Recalls
Hibiki has the ability to re-render previously defined stanzas automatically, and this can significantly reduce typing. In Hibiki, you can recall any previously defined stanza simply by typing its heading with an empty body. For example:
```
1 [Chorus]
2 I'm a chorus!
3 
4 [Chorus]
5 
```
The above is completely valid, and will result in the entirety of the `[Chorus]` stanza as it's defined on lines 1 and 2 to repeat on lines 4 and 5.

Of course, in order for this to work, you must have previously defined the stanza. Below is an example of an invalid Hibiki file:
```
1 [Verse 1]
2 
3 
```
No `[Verse 1]` has been previously defined, so Hibiki throws an `EmptyStanza` error.
# Chords
Stanzas contain a number of "lines" and each line is comprised of text followed by a newline character. These lines can also contain __chords__. (And if you'd like those defined, go learn music first.) Chords are denoted by some text inside of braces `{}` like so:
```
1 [Chorus]
2 {Am}I'm a {C}chorus!
3 
```
This results in the following output:
```
[Chorus]
Am    C
I'm a chorus!
```
Chords appear in the rendered output above the character immediately to the right of the chord definition. Hibiki supports chord definition of any type, and notably, __Hibiki does not speak to whether or not chords are valid.__ Hibiki's scope is not to say what chords are valid musically, only to identify them for the purpose of the language's syntax. To Hibiki, a chord `{H#m}` is seen as a valid chord, despite the fact that musically, it isn't.

Hibiki *does* however have special symbols which defined particular modifiers for chords.

# Repeats
Hibiki has the ability to automatically repeat individual lines as well as entire sections. This is done using rather intuitive syntax where you simply suffix the part you'd like to repeat with `(xn)`, where `n` is the number of repeats you'd like. In example:
```
1 [Chorus]
2 I'm a chorus! (x2)
3 
```
The above would result in line two appearing twice. You may also use this same method to repeat entire stanza:
```
1 [Chorus] (x2)
2 I'm a chorus!
3 
4 [Chorus]
5 
```
This results in the entire stanza - heading and all - being repeated twice after line 3. Notably though, stanza repeats do not carry across recalls. As an example, the recall appearing on line 4 would only have the heading and body printed once. If you want it repeated, you'd have to put the same `(x2)` after the recall.

# Line Recall
Hibiki also has the ability to save and recall individual lines. An example is shown below:
```
1 [Verse 1]
2 I'm a verse(=var)
3 Some other stuff
4 Remember me? (*var)
5 
```
This would result in the text `I'm a verse` being displayed normally on line 2, but this also has the effect of storing the contents in a variable named `var` in this case. Line 3 would display normally, and then line 4 would say `Remember me? I'm a verse`, recalling the contents of the variable `var` and appending it to the contents of line 4.

Lines are assigned to variables using parenthesis `()` and the equals sign `=` followed by the name of a variable. The name can be anything, but may only include letters, numbers, and underscores. __No spaces are allowed.__ The name of the variable used has no effect and is only for your own reference. Lines are recalled using parenthesis `()` and the asterisk `*` followed by the name of a variable previously defined.

Similar to stanza recalls, referencing a variable requires that the variable be previously defined. As an example, the Hibiki file below is invalid:
```
1 [Verse 1]
2 Some text (*some_var)
3 
```
This is because line two references a variable named `some_var`, but it's not defined elsewhere in the file. This would result in an `UndefinedRecall` error.

# Phantom Recall
Previously, all recalls we talked about require actually rendering text in order to perform. Sometimes however, a song contains a repeating phrase which appears all over the song, but which does not appear anywhere by itself. For this purpose, a "phantom recall" can be used.

It was mentioned earlier that __all text to be rendered must appear inside of a stanza__. This doesn't mean all text has to be in a stanza though, and we can leverage that fact to write a line recall which doesn't actually appear in the rendered version. Phantom recalls work identically to line recalls, but do not appear in stanzas. An example is shown below:
```
1 You can't see me here.(=phantom)
2 
3 [Chorus]
4 The statement below is false:
5 (*phantom)
6 
```
On line 1 - outside of a stanza, we define a line containing the text "You can't see me here." and store it in a variable named "phantom". Because this line appears outside of a stanza, it is not shown in the rendered output. Then on line 5 inside of the body of `[Chorus]`, we reference this variable, which results in the contents being rendered on line 5, resulting in the following output:
```
[Chorus]

The statement below is false:

You can't see me here.
```
