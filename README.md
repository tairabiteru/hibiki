# Hibiki
Hibiki is a language for programmatically creating musical tabs.

## What?
I play the ukulele. As such, I'm often reading tabs to play songs. I'm very particular about how my tabs are arranged.

1. Chords are written above the lyrics.
2. A chord appears immediately above the first letter of the syllable it corresponds to.
3. Each section of the song is denoted by a header in [brackets].
4. Reprisals can be referenced by simply putting the section's name in [brackets].

So, as an example:
```
[Chorus]
     C                         F
You  can't always get what you want
           D                  F
But if you try sometimes, you might find
                 C
You get what you need
```
The only problem with this arrangement is its creation: Typing out a bunch of spaces for the chords and positioning them is in my opinion, really annoying. I have seen tabs done a bit differently:
```
[Chorus]
You {C}can't always get what you {F}want
But if you {D}try sometimes, you {F}might find
You get what you {C}need
```
Which is easier to type, but doesn't look as nice. Well, what if we could convert between the two?

Yep. That's what this does.

## Features
- **Tokenization** - The framework Hibiki is built upon allows for chord recognition, and as a result, it can in theory be tied back to something like a system to show finger placement.
- **Section Recall** - Hibiki allows you to type a section like a `[Chorus]` out once, and then reference it later in code without having to retype the body. 

## FAQ
- **Why bother?** - Honestly, I write a lot of tabs. Something like this is genuinely useful to me, even if it only saves a bit of copying and pasting.
- **Ok, but is that really worth writing your own lexer?** I mean, I learn by doing, and being able to write lexers is something I want to be able to do. The thing is though, that's only part of it. Nearly all of the documents I have are digital, and I want my tabs to be too. However in spite of that, due to a myriad of factors, my tabs are still kept in a big binder with plastic sleeves. Granted, around a campfire, there's often no simpler way, but even if I had a device and electricity, screens themselves can be a problem. I once heard music described as "a game you play with yourself where the second you stop maintaining focus, you lose." That is *very* true for me, and having to fumble around with a mouse or a keyboard mid-song is not good for flow. Hibiki in that regard, is a stepping stone on the path to something grander which may one day allow for such digitization that isn't cumbersome to use. 

- **What's the meaning behind the name?** - "Hibiki" (響き) is the Japanese word for an "echo" or a "reverberation." 