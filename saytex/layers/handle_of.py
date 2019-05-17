"""
Handles the word "of". It should either be interpreted as a function,
say f(x) as "f of x", or it should be ignored (e.g., "integral of x")
"""

from .layer import SaytexLayer

import re

class HandleOfLayer(SaytexLayer):

    def execute_layer(self, input_string):
        """
        Handles the word "of" appropriately.
        """
        in_progress_string = input_string

        while True:
            # find the index
            ofindexmatch = re.search(r'\bof\b', in_progress_string)
            
            # if no of, then break
            if ofindexmatch == None:
                break

            ofindex = ofindexmatch.start()
            
            precedingstring = in_progress_string[:ofindex]

            followingstring = in_progress_string[ofindex + 2:]

            # check if of is preceded by integral or sum
            # TODO: recognize other constructs, such as "integral from 0 to infinity of x"
            # now, only "integral of x from 0 to infinity" would be properly recognized,
            # which is unfortunate
            if precedingstring.endswith('integral ') or precedingstring.endswith('sum ') or precedingstring.endswith('end '):
                # remove the of
                # and remove extra space
                in_progress_string = precedingstring.rstrip() + followingstring
                continue
            
            # check if of is preceded by possible function name
            # actually, for now, assume that this is always the case
            # get the next variable name
            followingstring = followingstring.lstrip()
            variablename = " " + followingstring.split(' ', 1)[0] + " "
            if len(followingstring) > len(variablename):
                followingstring = followingstring[len(variablename)-2:]
            else:
                followingstring = ""
            in_progress_string = precedingstring + "left parenthesis" + variablename + "right parenthesis" + followingstring
            




        return in_progress_string