# Hibiki
A language specifically to make writing musical tabs easier and more fun.

## The Problem With Writing Tabs
I very much enjoy playing the ukulele, and as a result, I often find myself writing my own tablature. While I like the process of discovering the correct chords, what I do *not* like is the act of writing the tabs themselves. I prefer my tabs to be written in a very particular manner:
```
[Intro]
Gm7
Is this the real life
C7
Is this just fantasy
Bbadd9      Cm7 F7
Caught in a landslide
    A#
No escape from reality
```
Chords positioned on every other line over the corresponding lyrics. A chord appears over the letters corresponding to the syllable upon which the chord falls. Except, oops! I made a mistake! That `Bbadd9` chord shouldn't be there; it should be an `F7` instead. Let's fix that:
```
[Intro]
Gm7
Is this the real life
C7
Is this just fantasy
F7      Cm7 F7
Caught in a landslide
    A#
No escape from reality
```
Ugh, now all of the other chords in that line got moved over because `F7` is shorter than `Bbadd9`. How annoying. Now I have to go in and manually add spaces.

All fine and good in this example. After all, it's just one chord, right? Sure, but what if this mistake occurred in a chorus, or a reprise? One where these incorrect chords have been reflected across the entire song?

Alas, there is a way to fix this. I've seen tabs written a different way:
```
[Intro]
{Gm7}Is this the real life
{C7}Is this just fantasy
{F7}Caught in a {Cm7}land{F7}slide
No e{A#}scape from reality
```
Well, that solves the chord spacing problem...but man, that looks ugly. What we really need is the best of both worlds. What if we could translate between the two?

## Enter, Hibiki
Hibiki is a...markup language? Sure, let's go with that. It is designed to basically do exactly what I described, with a few extra special features added in. Hibiki takes in "source code" like this:
```
[Intro]
{Gm7}Is this the real life
{C7}Is this just fantasy
{F7}Caught in a {Cm7}land{F7}slide
No e{A#}scape from reality
```
and turns it into tabs that look like this:
```
[Intro]
Gm7
Is this the real life
C7
Is this just fantasy
F7      Cm7 F7
Caught in a landslide
    A#
No escape from reality
```
Because we're writing inline with the lyrics, we don't have to worry about spacing anymore. If a chord is wrong, it can just be changed. In fact, Hibiki is also capable of re-rendering previous sections. As an example, this:
```
[Intro]
{Gm7}Is this the real life
{C7}Is this just fantasy
{F7}Caught in a {Cm7}land{F7}slide
No e{A#}scape from reality

[Intro]
```
turns into this:
```
[Intro]
Gm7
Is this the real life
C7
Is this just fantasy
F7      Cm7 F7
Caught in a landslide
    A#
No escape from reality

[Intro]
Gm7
Is this the real life
C7
Is this just fantasy
F7      Cm7 F7
Caught in a landslide
    A#
No escape from reality
```
Very nearly half the typing, and because `Intro` is only defined in one spot, if an alteration is made, you only have to make it once. You can even duplicate lines themselves!
```
[Intro]
{C} {F} {C} {F} (x4)
```
```
[Intro]
C F C F

C F C F

C F C F

C F C F

```
Hibiki also has a powerful feature called **recall**. This allows individual lines to be saved as "variables" which can then be recalled later in the song.
```
[Intro]
{C}I'm {Am}a recall!(=a_line)

[Outro]
Remember me? (@a_line)
```
```
[Intro]
C   Am
I'm a recall!

[Outro]
             C     Am
Remember me? I'm a recall!
```
Using a recall outside of a stanza allows you to declare information without it being rendered. This is called a **phantom recall**. It's useful when you, for example, have a chord progression that repeats all over a song, but isn't found anywhere by itself.
```
{Csus4} {C} {Csus2} {C}(=chords)

[Verse 1]
{C}Night (@chords) {Bb}fal{F}ls and I'm a{C}lone (@chords) {Bb} {F}
```
```
[Verse 1]
C     Csus4 C Csus2 C Bb F           C    Csus4 C Csus2 C Bb F
Night                 falls and I'm alone
```

## So like, why'd you do this?
*sigh*

Because "music is a game you play with yourself where the second you stop paying attention, you lose."

As it turns out, I'm *really* bad at paying attention. Anything - literally *anything* - I can do to make me focus more helps me, and that includes not being distracted by weird looking tabs. Of course as with learning any instrument, practice makes perfect, but I've found long ago that true greatness comes from passion. To skip the poetry, I have to *want* to play my ukulele. I have to *want* to learn weird chords. Does this help me do that? Directly, no, not really, but indirectly, yes. I love playing music but to play music, I need music to read. That means writing tabs out, and I *loathe* the process of writing them out. This makes that process not as bad, and a bit like programming (which I also like) and thus encourages me to write more tabs, and writing more tabs means more playing which means more practice which means personal growth, okay?

There is a second reason for this. In truth, this library - while useful - was not the final goal. Most of my tabs are on paper, and this is annoying to me because paper is bulky and wears out and can get lost, etc... So digitize them, obviously. But for a bunch of reasons I won't go into, that carries baggage with it too. This is a situation where I want an *extreme* level of control over a piece of software and...well, "if'n ya ain't got the right tool for the job, you're gonna might have to need to make 'er!" Hibiki acts as a library first and foremost, and that's because my personal implementation of this actually *extends* the functionality of Hibiki to create a web rendering system.

"So just because of the ridiculous level of control you want over the creation of musical tabs, you created your own quasi-tokenizer and language just to re-arrange some words on a page for you?"

Yeah, pretty much.
## Use
```Python
import hibiki

src = """[Intro]
{Gm7}Is this the real life
{C7}Is this just fantasy
{F7}Caught in a {Cm7}land{F7}slide
No e{A#}scape from reality
"""

tab = hibiki.Tab(src)

print(tab.render())
```
You can also use files:
```Python
tab.from_path("bohemian_rhapsody.hb")
print(tab.render())
```
Hibiki can also be invoked as a program in and of itself, directly from the command line:
```
python -m hibiki <somefile.hb>
```

## FAQ
- What's the meaning behind the name?
  - "hibiki" is a Japanese word meaning "echo" or "reverberation." This is adjacent to Hibiki's core function: ***echoing*** parts of tablature so you don't have to write them out yourself. Also "reverb" is music adjacent too.

