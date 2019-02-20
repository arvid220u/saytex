# SayTeX Language Master Document

In this document, a declaration of intent will be declared for the SayTeX language. We will define the scope and goals of SayTeX and SayTeX+.

The general idea is that to convert speech to LaTeX, we need to deal with two different problems: (1) that LaTeX commands use special symbols and commands that are hard to express in spoken language, and (2) that when math is spoken, there are usual several ways to say the same thing. Trying to solve these two problems with only one method is deemed to at best be cluttered and at worst fail to solve either of the two problems. In this document, I will therefore detail a way to split these tasks into two languages, SayTeX and SayTeX+, and explain how they relate to each other and to speech and LaTeX.

## SayTeX

Let's start with SayTeX, which aims to solve problem (1), namely that LaTeX commands are hard to pronounce. What follows is a list of properties that SayTeX syntax must follow:

1. One-to-one mapping to LaTeX. No exceptions. (hmm. raw mode? allow numbers both as words and sequence of digits? allow plus signs?)
2. Easy to pronounce. No special symbols and no numbers. Only words and letters.
3. Case insensitive.
4. Linear-time conversion to LaTeX.

## SayTeX+

SayTeX+ addresses problem (2), namely that spoken math is not one-to-one with LaTeX. SayTeX+ has no formal syntax requirements, other than that it should be possible to unambiguously convert SayTeX+ to SayTeX. What follows is a non-exhaustive list of possible features that SayTeX+ can have:

- Shorthand syntax for common expressions. For example, "a over b" could convert to "fraction begin a end begin b end".
- Automatically inserted spaces. For example, in integrals, a space could be inserted.
- Adaptations for typing, such as converting "A" to "capital a".
- Recognition of LaTeX within SayTeX+ expression.
