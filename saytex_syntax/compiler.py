"""
Defines the SaytexSyntax class, containing methods for converting between SayTeX and LaTeX.
"""

import syntax_dictionary


class SaytexSyntaxError(Exception):
    """
    Raised in to_latex, if error.
    """
    pass

class LatexParsingError(Exception):
    """
    Raised in from_latex, if error.
    """
    pass


class SaytexSyntax:
    """
    Contains methods to_latex and from_latex for converting between LaTeX
    and SayTeX syntax. Also supports reloading of the syntax dictionary.
    """

    def __init__(self):
        """
        Initializes SaytexSyntax. Specifically, a syntax dictionary will be loaded.
        """
        # load the syntax dictionary from the SYNTAX_FILE specified in syntax_dictionary
        self.load_syntax_dictionary(syntax_dictionary.SYNTAX_FILE)


    def load_syntax_dictionary(self, syntax_file):
        """
        Load the syntax dictionary as self.syntax_dictionary.
        """
        self.syntax_dictionary = syntax_dictionary.SyntaxDictionary(syntax_file)


    def to_latex(self, saytex_string):
        """
        Converts SayTeX Syntax into LaTeX code.
        :param saytex_string: A string containing valid SayTeX Syntax code.
        If it is not valid SayTeX Syntax, a SaytexSyntaxError will be raised.
        :return: A string containing a valid translation of the input string into LaTeX. 
        """

        # naively, it should just do linear-time string matching using the dictionary
        # maybe, there might arise situations where a dp-based approach could profitably be used
        # i do not expect that to every arise, but it can't really hurt to implement it that way,
        # if anyway that scenario never occurs.
        # therefore, do the DP thing. we need to have some sort of limit at the number of words
        # in saytex. maybe max 3 words? max 5 words? should not affect the runtime at all
        # i'd say 5 words. needs to be explicitly defined in saytex-syntax-v01.txt

        pass



        