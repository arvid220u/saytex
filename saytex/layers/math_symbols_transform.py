"""
Transforms symbols such as '+' and '*'
into the words 'plus' and 'times'
"""

from .layer import SaytexLayer

import re

class MathSymbolsTransformLayer(SaytexLayer):

    SYMBOLS = {
        '+': 'plus',
        '*': 'times',
        '-': 'minus',
    }

    def execute_layer(self, input_string):
        """
        Transforms all symbols into words for the symbols.
        """
        in_progress_string = input_string

        for symbol in MathSymbolsTransformLayer.SYMBOLS:
            in_progress_string = re.sub('\\s*\\' + symbol + '\\s*', " " + MathSymbolsTransformLayer.SYMBOLS[symbol] + " ", in_progress_string)

        return in_progress_string
