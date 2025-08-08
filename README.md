# Hibiki
A language specifically to make writing musical tabs easier and more fun by turning the act of writing tabs into programming. Hibiki is designed to take "tab source code" like this:
```
took the {G}midnight train goin' {G#m}anywhere{A}(=train)

[Intro]
{E} {B} {C#m} {A}
{E} {G} {G#m} {A}

[Verse 1]
{E}  Just a {B}small town girl, {C#m} livin' in a {A}lonely world
{E}  She (@train)
{E}  Just a {B}city boy, {C#m} born and raised in {A}South Detroit
{E}  (@train)

[Intro]
```
and turn it into this:
```
[Intro]
E B C#m A

E B G#m A

[Verse 1]
E        B                C#m             A
  Just a small town girl,     livin' in a lonely world
E              B                    G#m     A
  She took the midnight train goin' anywhere
E        B        C#m                    A
  Just a city boy,    born and raised in South Detroit
E             B                    G#m     A
  He took the midnight train goin' anywhere

[Intro]
E B C#m A

E B G#m A
```
## Why
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
Hibiki is a...markup language? Sure, let's go with that. It is designed to basically do exactly what I described, with a few extra special features added in. Because we're writing inline with the lyrics, we don't have to worry about spacing anymore. If a chord is wrong, it can just be changed. In fact, Hibiki is also capable of re-rendering previous sections. As an example, this:
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
- **This seems a lot more complicated than just writing out tabs.**
  - That's not a question, but fine. I'll elaborate. I realize the intersection of the set of people who play music and the set of all people who program is pretty small, but **I'm** in that intersection, and regarding music, I'd once heard it said,

    **"Music is a game you play with yourself where the second you stop paying attention, you lose."**

    As it happens, I'm really bad at paying attention. Thusly, having neat and tidy tabs is ***SUPER*** important to me. The level of control I want over my tabs is far above what any pre-built solution I've seen out there can provide, and...well, "If'n ya ain't got the right tool for the job, you're gonna might have to need to make 'er!"

    Thus, Hibiki as a concept was born.
- **So you made your own quasi-tokenizer just to write musical tabs?**
  - Yeah, pretty much.

    I mean, there's slightly more to it that that: I believe the number one ingredient in success is passion. To skip the poetry, I want to be good at playing the ukulele. To get good, it is my belief that I have to *WANT* it. Obviously, but the realm of "wanting it" doesn't stop at the act itself. Taking steps to do things which *encourage me* to practice is also important. 

    Basically, Hibiki helps me write tabs. It helps my programmer brain not be so upset at how badly I'm repeating myself when writing tabs. Because I'm more likely to write tabs using Hibiki, I'll end up creating more tabs to read. Since I have more tabs to read, I'll play more, which means I'll be practicing more, which means personal growth. 

    Writing tabs this way will definitely not appeal to everyone, especially those who don't want to lean on any software to write tabs. But to me, the most important aspect of Hibiki is its appeal to ***ME***. If anyone else finds it useful too, cool. Enjoy.
- **What's the meaning behind the name?**
  - "hibiki" is a Japanese word meaning "echo" or "reverberation." This is adjacent to Hibiki's core function: ***echoing*** parts of tablature so you don't have to write them out yourself. Also "reverb" is music adjacent too.

