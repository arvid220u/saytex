"""
Defines a SyntaxDictionary class which handles reading from a SayTeX Syntax file.
"""

import json

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
        # the syntax file must have the correct format, as specified in config.py
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
        for i, syntax_item in enumerate(self.syntax_list):
            if "saytex" not in syntax_item or "latex" not in syntax_item:
                raise InvalidSyntaxFile
            # provide default spacing
            if "right_space" not in syntax_item:
                self.syntax_list[i]["right_space"] = 1
            if "left_space" not in syntax_item:
                self.syntax_list[i]["left_space"] = 1
        
        # create the syntax_dictionary from saytex to an index in the syntax_list
        self.syntax_dictionary = {}
        for syntax_index, syntax_item in enumerate(self.syntax_list):
            self.syntax_dictionary[syntax_item["saytex"]] = syntax_index
    
    def get_latex(self, saytex):
        """
        Returns the corresponding latex code for saytex, and None if saytex
        is an invalid command. The latex code will be space padded according
        to the value in the dictionary.
        :param saytex: str, containing potential saytex command
        """
        if saytex not in self.syntax_dictionary:
            return None
        syntax_entry = self.syntax_list[self.syntax_dictionary[saytex]]
        command = syntax_entry["latex"]
        command = " "*syntax_entry["left_space"] + command + " "*syntax_entry["right_space"]
        return command
    


