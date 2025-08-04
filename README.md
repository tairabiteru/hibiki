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

## FAQ
- What's the meaning behind the name?
  - "hibiki" is a Japanese word meaning "echo" or "reverberation."

