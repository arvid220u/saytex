"""
Makes the input treated as case insensitive, which is what it
should be if coming from spoken language.
"""

from .layer import SaytexLayer

class CaseInsensitivityLayer(SaytexLayer):

    def execute_layer(self, input_string):
        """
        Transforms all capital letters into lowercase letters.
        """
        in_progress_string = input_string

        in_progress_string = in_progress_string.lower()

        return in_progress_string