"""
Defines a SyntaxDictionary class which handles reading from a SayTeX Syntax file.
"""

import json
import pkg_resources
from . import config

class InvalidSyntaxFile(Exception):
    """
    Raised if the syntax json file is not of valid format.
    """
    pass

class UnrecognizedSaytexCommand(Exception):
    pass

class SyntaxDictionary:
    """
    Represents a Syntax Dictionary.
    """

    def __init__(self, syntax_file=None, syntax_directory=None):
        """
        Initializes a new SyntaxDictionary using the syntax_file or syntax_directory.
        Raises exception not exactly one of syntax_file and syntax_directory is None.
        """
        # set the syntax file
        # the syntax file must have the correct format, as specified in config.py
        self.syntax_file = syntax_file
        # set the syntax directory
        self.syntax_directory = syntax_directory

        # make sure that exactly one of them is None
        if syntax_file == None and syntax_directory == None:
            raise Exception("Either syntax_file or syntax_directory required.")
        if syntax_file != None and syntax_directory != None:
            raise Exception("Only one of syntax_file and syntax_directory can be provided.")

        # interpret the syntax file
        # this will raise an error if the syntax file is wrongly formatted
        self.load_syntax()
    

    def load_syntax(self):
        """
        Loads the syntax defined in self.syntax_file or self.syntax_directory into
        the array self.syntax_list and the dictionary self.syntax_dictionary.
        """
        if self.syntax_file != None:
            with open(pkg_resources.resource_filename(__name__, self.syntax_file), 'r') as sf:
                self.syntax_list = json.load(sf)
        elif self.syntax_directory != None:
            self.syntax_list = []
            for f in pkg_resources.resource_listdir(__name__, self.syntax_directory):
                with open(pkg_resources.resource_filename(__name__, self.syntax_directory + "/" + f), 'r') as sf:
                    self.syntax_list.extend(json.load(sf))
        else:
            # should never happen!
            raise Exception("Both syntax_file and syntax_directory are None; cannot load syntax.")

        # make sure that the syntax is correctly formatted
        for syntax_item in self.syntax_list:
            if "saytex" not in syntax_item or "latex" not in syntax_item:
                raise InvalidSyntaxFile("Every element needs to have a saytex field and a latex field")
            # the length of the saytex command is limited by config
            if len(syntax_item["saytex"].split(" ")) > config.MAX_WORDS_PER_SAYTEX_COMMAND:
                raise InvalidSyntaxFile("Length of SayTeX command exceeds max length: " + syntax_item["saytex"])
            # provide default values
            self.make_syntax_entry_default(syntax_item)
            
        
        # create the syntax_dictionary from saytex to an index in the syntax_list
        self.syntax_dictionary = {}
        for syntax_index, syntax_item in enumerate(self.syntax_list):
            # make sure that there is no command appearing twice
            if syntax_item["saytex"] in self.syntax_dictionary:
                raise InvalidSyntaxFile("SayTeX command appearing twice: " + syntax_item["saytex"])
            self.syntax_dictionary[syntax_item["saytex"]] = syntax_index

    def make_syntax_entry_default(self, syntax_item):
        """
        Modifies the supplied syntax entry d, to add default values for parameters.
        
        :param syntax_item: A dictionary representing a syntax entry to be modified in place.
        """
        if "right_space" not in syntax_item:
            syntax_item["right_space"] = 1
        if "left_space" not in syntax_item:
            syntax_item["left_space"] = 1
        if "insert_curly_brackets_right" not in syntax_item:
            syntax_item["insert_curly_brackets_right"] = False


    def get_latex(self, saytex, params = {}):
        """
        Returns the corresponding latex code for saytex, and None if saytex
        is an invalid command. The latex code will be space padded according
        to the value in the dictionary.
        
        :param saytex: str, containing a potential saytex command
        :param params: dict, containing params to be passed to post_process_latex
        
        :return: a post processed str, or None if saytex is not a valid command
        """
        try:
            syntax_entry = self.get_syntax_entry(saytex)
        except UnrecognizedSaytexCommand:
            return None
        
        return self.post_process_latex(syntax_entry, **params)
    
    def get_syntax_entry(self, saytex):
        """
        Returns a syntax entry corresponding to saytex, if exists.
        Otherwise, raises KeyError.
        
        :param saytex: str, containing a potential saytex command
        
        :return: a dictionary in self.syntax_list
        """
        if saytex not in self.syntax_dictionary:
            raise UnrecognizedSaytexCommand("The command " + saytex + " is not recognized.")
        syntax_entry = self.syntax_list[self.syntax_dictionary[saytex]]
        return syntax_entry

    def post_process_latex(self, syntax_entry, insert_curly_brackets = False):
        """
        Returns the post processed version of the syntax_entry, by adding spacing
        or curly brackets.
        
        :param syntax_entry: a dictionary that could be a member of syntax_list
        :param insert_curly_brackets: bool, indicating whether the latex
            command should be curly bracket padded instead of space padded
        
        :return: str, the post processed version
        """
        latex_command = syntax_entry["latex"]

        if insert_curly_brackets:
            latex_command = "{" + latex_command + "}"

        # space padding
        final_command = " "*syntax_entry["left_space"] + latex_command + " "*syntax_entry["right_space"]

        return final_command

    def get_next_params(self, saytex):
        """
        Returns a (possibly empty) dictionary containing the params that should
        be passed to the next call of post_process_latex
        
        :param saytex: str, containing a potential saytex command
        """
        if saytex not in self.syntax_dictionary:
            return {}
        syntax_entry = self.syntax_list[self.syntax_dictionary[saytex]]
        return {"insert_curly_brackets": syntax_entry["insert_curly_brackets_right"]}

