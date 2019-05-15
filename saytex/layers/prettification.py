"""
Does various things to produce prettier LaTeX strings, such as
inserting spaces into integrals.
"""

from .layer import SaytexLayer

import re

class PrettificationLayer(SaytexLayer):

    def execute_layer(self, input_string):
        """
        Adds spaces to integrals to produce prettier equations.
        """
        in_progress_string = input_string

        # more prettification measures should be taken, but for now,
        # only do insertion of spaces into integrals

        # idea: find a d$, where $ can be any character, and check if there is
        # an integral preceding it


        for integrandmatch in re.finditer(r'\bd[a-z]\b', in_progress_string):
        
            integrandindex = integrandmatch.start()

            if "integral" not in in_progress_string[:integrandindex]:
                continue
            
            precedingstring = in_progress_string[:integrandindex]

            followingstring = " " + in_progress_string[integrandindex:]

            in_progress_string = precedingstring + "small space" + followingstring

        return in_progress_string