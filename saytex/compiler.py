"""
Defines the Saytex class, containing methods for converting between
natural language and LaTeX. The conversion is done in a two-step process 
by first translating the input into SayTeX Syntax, after which the 
saytexsyntax module is used for the final LaTeX conversion.
"""

from . import config

from .saytexsyntax import SaytexSyntax

from .layers import SaytexLayer

class UnrecognizableSaytexInput(Exception):
    """
    Raised in to_latex and to_saytex, if the input cannot be transformed 
    into valid SayTeX Syntax.
    """
    pass

class Saytex:
    """
    Contains the method to_latex to convert from natural
    language to LaTeX. It will do this by invoking the layers
    defined in config.py in the specified order, followed by a
    final call to SaytexSyntax. The method to_saytex will do the
    same thing, without the call to SaytexSyntax.
    """

    def __init__(self):
        """
        Initializes a Saytex instance. Specifically, an instance of
        SaytexSyntax will be initialized as well.
        """
        self.saytex_syntax_compiler = SaytexSyntax()


    def to_latex(self, math_string):
        """
        Converts natural language into LaTeX code.
        :param math_string: A string containing a spoken math expression. The
        string should use the SayTeX+ format, which is a superset of
        SayTeX Syntax.
        :return: A string containing a valid translation of the input string
        to LaTeX code. If the string does not conform to SayTeX+ (which
        can only happen if it uses unallowed characters), the
        InvalidSaytexPlus exception will be raised.
        """
        
        # convert into saytex
        saytex_syntax = self.to_saytex(math_string)

        # saytex syntax to latex
        latex = self.saytex_syntax_compiler.to_latex(saytex_syntax)

        return latex
    
    def to_saytex(self, math_string):
        """
        Converts natural language into SayTeX Syntax.
        :param math_string: A string containing a spoken math expression. The
        string should use the SayTeX+ format, which is a superset of
        SayTeX Syntax.
        :return: A string containing a valid translation of the input string
        to SayTeX Syntax. If the string is not recognizable (that is, it
        cannot be converted into SayTeX), the UnrecognizableSaytexInput exception 
        is thrown.
        """

        # the idea is to use a layering approach, where the string goes through
        # a bunch of transformations until finally becoming pure saytex
        
        # in_progress_string contains the string as it is being converted into saytex
        in_progress_string = math_string

        # get all layers that should be used
        layers = [layer for layer in config.used_layers if config.used_layers[layer]]

        # sort the layers by priority
        # lowest priority comes first (yes, i know, not ideal naming there)
        layers.sort(key = lambda layer_id : config.layer_priorities[layer_id])

        # now apply the layers
        for layer_id in layers:
            layer = SaytexLayer.get_layer(layer_id)
            in_progress_string = layer.execute_layer(in_progress_string)

        # the string that is the result of all layer executions
        saytex_syntax = in_progress_string

        # return the saytex syntax
        return saytex_syntax