"""
Maps common ways of expressing math formulas into
the specific SayTeX Syntax way of saying things.
"""

from .layer import SaytexLayer

import re

class SynonymStandardizationLayer(SaytexLayer):


    def execute_layer(self, input_string):
        """
        Converts common synonyms into SayTeX Syntax equivalents.
        """
        in_progress_string = input_string

        # use the syntaxdictionary structure

        return in_progress_string