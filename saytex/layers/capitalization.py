"""
Recognizes the keyword "capital" to capitalize the following
word.
"""

from .layer import SaytexLayer

import re

class CapitalizationLayer(SaytexLayer):

    def execute_layer(self, input_string):
        """
        Transforms "capital a" into "A", for example.
        """
        in_progress_string = input_string

        # basically, we just transform the first letter of the next word
        # to its uppercase version
        in_progress_string = re.sub(r'\bcapital (\D)', lambda x : x.group(1).upper(), in_progress_string)

        return in_progress_string