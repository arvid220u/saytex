Using the Python Package
========================

The ``saytex`` Python package consists mainly of the ``Saytex`` class.
It contains the method ``to_latex`` which takes a string as its input and
outputs a well-formatted LaTeX string.

A simple example of how to use the ``Saytex`` class is shown below:

::

    from saytex import Saytex

    saytex_compiler = Saytex()

    print(saytex_compiler.to_latex("a squared plus b"))

As one would expect, the above code prints ``a^2 + b``, which is the valid LaTeX translation of that string.
