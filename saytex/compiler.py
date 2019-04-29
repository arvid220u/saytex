"""
Defines the Saytex class, containing methods for converting between
natural language and LaTeX. The conversion is done in a two-step process 
by first translating the input into SayTeX Syntax, after which the 
saytexsyntax module is used for the final LaTeX conversion.
"""

import config

from saytexsyntax import SaytexSyntax

class UnrecognizableSaytexInput(Exception):
    """
    Raised in to_latex and to_saytex, if the input cannot be transformed into valid SayTeX Syntax.
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
        to SayTeX Syntax. If the string does not conform to SayTeX+ (which
        can only happen if it uses unallowed characters), the
        InvalidSaytexPlus exception will be raised.
        """

        # the idea is to use a layering approach, where the string goes through
        # a bunch of transformations until finally becoming pure saytex
        
        # in_progress_string contains the string as it is being converted into saytex
        in_progress_string = math_string

        # TODO: transformations

        saytex_syntax = in_progress_string

        return saytex_syntax