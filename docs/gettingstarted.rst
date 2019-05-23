Getting Started
==================



.. _installation:

Installation
---------------

SayTeX exists as a Python 3 package, which allows you to use the SayTeX functionality
from any Python module or script.

Install the ``saytex`` package using PyPI:

.. code-block:: bash

    pip install saytex

Note that the ``saytex`` package only supports Python 3. If the above
command gives an error, run ``pip -V`` and make sure it says Python 3. If
it does not, try running ``pip3`` instead.





Simple Usage
---------------

The ``saytex`` Python package consists mainly of the ``Saytex`` class.
It contains the method ``to_latex`` which takes a string as its input and
outputs a well-formatted LaTeX string.

A simple example of how to use the ``Saytex`` class is shown below:

::

    from saytex import Saytex

    saytex_compiler = Saytex()

    print(saytex_compiler.to_latex("a squared plus b"))

As one would expect, the above code prints ``a^2 + b``, which is the valid LaTeX translation of that string.

For notes on how to configure SayTeX to suit specific needs, see the :ref:`advanced-usage`.