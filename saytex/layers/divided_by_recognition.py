"""
Recognizes the word 'over' and transforms it into a properly
formatted fraction (fraction begin ... end begin ... end)
"""

from .layer import SaytexLayer

import re

class DividedByRecognitionLayer(SaytexLayer):

    def execute_layer(self, input_string):
        """
        Transforms "a over b" into "fraction begin a end begin b end".
        """
        in_progress_string = input_string

        raise NotImplementedError