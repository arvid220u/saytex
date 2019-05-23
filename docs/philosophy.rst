.. _philosophy:

Philosophy
=================

To convert spoken math to LaTeX, we need to deal with two
different problems: (1) that LaTeX commands use special symbols and commands that
are hard to express in spoken language, and (2) that when math is spoken, there are
usually several ways to say the same thing. Trying to solve these two problems with only
one method is deemed to at best be cluttered and at worst fail to solve either of the
two problems. Instead, SayTeX solves each problem separately, through the introduction
of the intermediary SayTeX Syntax.

When SayTeX receives a math string, it first converts it heuristically to SayTeX Syntax,
which is then converted unambiguously to LaTeX. Enforcing this split, along with a few
other key invariants, enables SayTeX to solve both of the previously outlined problems
at once.


SayTeX Syntax
----------------

SayTeX Syntax can be thought of as a pronounceable version of LaTeX. The following
list outlines some key properties that guided the design of SayTeX Syntax:

1. One-to-one mapping to LaTeX. No exceptions. 
2. Easy to pronounce.
3. No special symbols.
4. Only words and numbers.
5. Case sensitive.
6. Linear-time conversion to LaTeX.

The full specifications for SayTeX Syntax can be found in :ref:`saytex-syntax`. Some examples
are listed below.

- ``a plus b superscript 2`` = ``a + b^2``
- ``fraction begin x plus y end begin pi end`` = ``\frac{x + y}{\pi}``
- ``inverse hyperbolic cotangent left parenthesis x right parenthesis`` = ``\arcoth \left( x \right)``

It is simple to convert from SayTeX Syntax to LaTeX using the ``saytex`` package:

::

    from saytex import SaytexSyntax

    saytex_syntax = SaytexSyntax()

    print(saytex_syntax.to_latex("a plus b superscript 2"))

Note that since SayTeX Syntax should be in one-to-one correspondence with LaTeX,
any LaTeX can be converted into SayTeX Syntax, which could potentially
be useful for screen readers when encountering LaTeX. The ``to_saytex``
method is not yet implemented, however.


Natural Language to SayTeX Syntax
--------------------------------------------

SayTeX Syntax addresses the problem of making LaTeX easily pronounceable. As can
be seen in the examples above, however, SayTeX Syntax is restrictive
and verbose, making it less than ideal for regular use. SayTeX therefore employs
a number of heuristics to convert common ways of expressing math into SayTeX
Syntax.

SayTeX does not enforce any formal restrictions on its input. Rather, the
set of recognizable strings is implementation-specific.

The natural language to SayTeX conversion is implemented using layers; each layer
takes as input the output of the layer preceding it. More details on the implementation
can be found in :ref:`advanced-usage`. The following is the list of default
layers:

- Correct common speech recognition mistakes, such as "eggs" instead of "x".
- Transform the input to lowercase.
- Recognize the word "capital" to capitalize the next word. For example, "capital a" would become "capital A".
- Recognize spoken numbers, such as "three hundred and fifty six" for "356".
- Convert synonyms into the canonical SayTeX Syntax version. For example, "multiplied by" should become "centered dot".
- Recognize expressions on the form "integral from ... to ... of ...".
- Convert "a over b" into "fraction begin a end begin b end".
- Prettify the output, e.g. by inserting a space before the "dx" in an integral.

Each of these layers can be disabled if so desired, and users of the package
can easily add their own layers. An important note is that all valid SayTeX Syntax
should remain valid after passing through all layers. By enforcing this,
we guarantee that virtually any LaTeX expression can be recognized by SayTeX,
while at the same time providing shorthand syntax for the most common usecases.

