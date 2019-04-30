"""
Recognizes the keyword "capital" to capitalize the following
word.
"""

from .layer import SaytexLayer

class CapitalizationLayer(SaytexLayer):

    def execute_layer(self, input_string):
        """
        Transforms "capital a" into "A", for example.
        """
        in_progress_string = input_string


        return in_progress_string