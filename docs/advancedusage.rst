.. _advanced-usage:

Advanced Usage
================

Note: It is recommended to read :ref:`philosophy` before this section.


Interfacing with SayTeX Syntax
---------------------------------

A recognizable SayTeX string can be compiled into a SayTeX Syntax string,
as shown below.

::

    from saytex import Saytex

    saytex_compiler = Saytex()

    print(saytex_compiler.to_saytex("a plus b to the power of two"))

A valid SayTeX Syntax string can then be compiled into LaTeX:

::

    from saytex import SaytexSyntax

    saytex_syntax = SaytexSyntax()

    print(saytex_syntax.to_latex("a plus b superscript 2"))

Note that cascading these two methods produces exactly the same result
as the ``saytex.Saytex.to_latex`` method.

A SayTeX Syntax string can be validated using the ``saytex.saytexsyntax.SaytexSyntax.is_valid_saytex_syntax``
method.

In-depth reference can be found in :ref:`_saytexsyntaxreference`.


Configuring SayTeX Layers
---------------------------

The SayTeX-to-SayTeX-Syntax conversion is done through layers, with each layer's output
being the input to the next layer. The ``Saytex`` class comes with a number of pre-defined
layers (as outlined in :ref:`philosophy`), which are good for usage in a general speech-recognition
setting, but might not be perfect in all usecases.

To remove an existing layer, use the ``Saytex.remove_layer`` function:

::

    from saytex import Saytex
    import saytex.layers.prettification.PrettificationLayer as PrettificationLayer

    saytex_compiler = Saytex()

    saytex_compiler.remove_layer(PrettificationLayer)

One can also create completely new layers by subclassing ``saytex.layers.Layer`` and implementing
the ``execute_layer`` function:

::
    import saytex.layers.Layer

    class ExampleLayer(saytex.layers.Layer):

        def execute_layer(input_string):
            """
            This example layer adds "implies zero equals zero" to all input strings.
            """
            return input_string + " implies zero equals zero"
    
This layer can then be added to the ``saytex_compiler``. When doing that, a priority
needs to be specified, which indicate where in the sequence of layers the new layer
should be executed. The default priorities can be found here.

::

    saytex_compiler.add_layer(ExampleLayer, 4)

After this, when running ``saytex_compiler.to_latex`` or ``saytex_compiler.to_saytex``,
the compiler will not prettify the output, but it will always add "implies zero equals zero"
to all 