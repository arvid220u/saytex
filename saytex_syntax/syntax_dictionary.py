"""
Defines a SyntaxDictionary class which handles reading from a SayTeX Syntax file.
"""

import json

"""
The path to the syntax file.
The syntax file must be in json format, being an array in which
every element has at least two fields: "saytex" representing the
SayTeX Syntax command, and "latex" representing the corresponding
LaTeX command or symbol.
"""
SYNTAX_FILE = "saytex_dictionary.json"

class InvalidSyntaxFile(Exception):
    """
    Raised if the syntax json file is not of valid format.
    """
    pass

class SyntaxDictionary:
    """
    Represents a Syntax Dictionary.
    """

    def __init__(self, syntax_file):
        """
        Initializes a new SyntaxDictionary using the syntax_file.
        Raises exception if the syntax_file
        """
        # set the syntax file
        self.syntax_file = syntax_file

        # interpret the syntax file
        # this will raise an error if the syntax file is wrongly formatted
        self.load_syntax()
    

    def load_syntax(self):
        """
        Loads the syntax defined in self.syntax_file into
        the array self.syntax_list and the dictionary
        self.syntax_dictionary.
        """
        with open(self.syntax_file, 'r') as sf:
            self.syntax_list = json.load(sf)
            
        # make sure that the syntax is correctly formatted
        for syntax_item in self.syntax_list:
            if "saytex" not in syntax_item or "latex" not in syntax_item:
                raise InvalidSyntaxFile
        
        # create the syntax_dictionary from saytex to latex
        self.syntax_dictionary = {}
        for syntax_item in self.syntax_list:
            self.syntax_dictionary[syntax_item["saytex"]] = syntax_item["latex"]
    
    def get_latex(self, saytex):
        """
        Returns the corresponding latex code for saytex, and None if saytex
        is an invalid command.
        :param saytex: str, containing potential saytex command
        """
        if saytex not in self.syntax_dictionary:
            return None
        return self.syntax_dictionary[saytex]
    


