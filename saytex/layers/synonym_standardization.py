"""
Maps common ways of expressing math formulas into
the specific SayTeX Syntax way of saying things.
"""

from .layer import SaytexLayer

import re

import json
import pkg_resources

class SynonymStandardizationLayer(SaytexLayer):

    
    def __init__(self):
        super().__init__()

        self.syntax_dictionary = SynonymStandardizationDictionary(syntax_file="synonym_standardization_dictionary.json")


    def execute_layer(self, input_string):
        """
        Converts common synonyms into SayTeX Syntax equivalents.
        """
        in_progress_string = input_string

        in_progress_string = self.convert_synonyms(in_progress_string)

        return in_progress_string

    

    def convert_synonyms(self, saytex_string, word_list = None, word_index = 0, dp_memo = None):
        """
        Converts SayTeX Syntax into LaTeX code.

        :param saytex_string: A string containing valid SayTeX Syntax code.
        :param word_list (optional): A list of tokenized words derived from saytex_string.
            If word_list is not None, then the saytex_string will be ignored. Is normally only used
            for recursive calls.
        :param word_index: The current index in the word_list that we are at. Used in recursive calls.
            If it is not valid SayTeX Syntax, a SaytexSyntaxError will be raised.
        :param dp_memo: A dictionary mapping indices in the word_list to generated LaTeX strings.
        :param next_params: A dictionary of parameters to be passed to the next get_latex call.
        
        :return: A string containing a valid translation of the input string into LaTeX (if no exception).
            If word_index > 0, the return value is a tuple (string, value) where value is a measure of
            how good the string is as a LaTeX translation of saytex_string.
        """

        # initialize dp_memo
        if dp_memo == None:
            dp_memo = {}

        # if the word_index is in our dp_memo, then return that
        if word_index in dp_memo:
            if type(dp_memo[word_index]) == UnrecognizedSynonym:
                raise dp_memo[word_index]
            return dp_memo[word_index]


        # if word_list is None, tokenize the saytex_string
        if word_list == None:
            # split by space
            word_list = saytex_string.split()

        # if index is greater than or equal to the length of the word list,
        # we can safely return an empty string with value 0. this is our base case.
        if word_index >= len(word_list):
            dp_memo[word_index] = ("", 0)
            return dp_memo[word_index]
        
        # contains tuples on the form (latex, value) where latex is a string containing
        # the latex representation of word_list[word_index:], and value is an integer
        # representing the number of non-commands we have used to get to this expression
        # generally, we will want to minimize the value
        possible_answers = []

        # iterate over all possible command lengths, now
        for command_length in range(1,10):
            # break if too far
            if word_index + command_length > len(word_list):
                break
            command_index_end = word_index + command_length
            command = " ".join(word_list[word_index:command_index_end])
            # if this is a real command, it should not need curly brackets
            try:
                self.syntax_dictionary.get_syntax_entry(command)
            except UnrecognizedSynonym:
                pass
            # get the latex
            latex = self.syntax_dictionary.get_standard_synonym(command)
            # if latex is not None, recurse
            if latex != None:
                try:
                    ans = self.convert_synonyms("", word_list=word_list, word_index=command_index_end, dp_memo=dp_memo)
                    # do not increase the value
                    possible_answers.append((latex + " " + ans[0], ans[1]))
                except UnrecognizedSynonym:
                    pass
            else:
                # if the length of the command is 1, we could possibly interpret this command as an actual word/number
                # that should just be literally transcribed into latex
                # remember that by the way we deal with spaces, we need to space-pad a word
                # also, we want to increase the value since this is not ideal
                if command_length == 1:
                    # build a syntax entry for the word
                    word = word_list[word_index]
                    # if the word only has a single character, then one should not insert brackets
                    try:
                        ans = self.convert_synonyms("", word_list=word_list, word_index=command_index_end, dp_memo=dp_memo)
                        possible_answers.append((word + " " + ans[0], ans[1] + 1))
                    except UnrecognizedSynonym:
                        pass
        
        if len(possible_answers) == 0:
            # we found no possible translations of this string into latex
            # this should never happen, since we can just keep adding regular words instead
            raise UnrecognizedSynonym("If you get this error, something is deeply wrong with this code.")
        
        # now, return the answer with the minimal value
        chosen_answer = possible_answers[0]
        for a in possible_answers[1:]:
            if a[1] < chosen_answer[1]:
                chosen_answer = a
        
        # return an error if there are multiple answers with the same value
        answer_count = 0
        for a in possible_answers[1:]:
            if a[1] == chosen_answer[1]:
                answer_count += 1
                if answer_count >= 2:
                    raise UnrecognizedSynonym("The following expression has more than 1 possible interpretation: " \
                                                        + str(word_list) + " at index " + str(word_index) + \
                                                        ". The possible interpretations are: " \
                                                        + chosen_answer[0] + " and " + a[0] + ". Possible answers: " + \
                                                        str(possible_answers))

        # if index is not 0, this is what we should return
        if word_index != 0:
            dp_memo[word_index] = chosen_answer
            return chosen_answer

        # if the index is 0, we need to make additional adjustments
        # for example, we need to return a string, not a tuple
        # also, we want to strip the answer
        chosen_latex_string = chosen_answer[0]
        # strip spaces
        chosen_latex_string = chosen_latex_string.strip(" ")
    
        # return the string
        return chosen_latex_string





class InvalidSynonymStandardizationDictionary(Exception):
    pass
class UnrecognizedSynonym(Exception):
    pass


class SynonymStandardizationDictionary:
    """
    Works as an interface for the synonym standardization dictionary.
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
        the array self.syntax_list and the dictionary
        self.syntax_dictionary.
        """
        if self.syntax_file != None:
            self.syntax_list = []
            with open(pkg_resources.resource_filename(__name__, self.syntax_file), 'r') as sf:
                for syntax_entry in json.load(sf):
                    for from_word in syntax_entry["from"]:
                        self.syntax_list.append({'to': syntax_entry['to'], 'from': from_word})
                    self.syntax_list.append({'to': syntax_entry['to'], 'from': syntax_entry['to']})
        elif self.syntax_directory != None:
            self.syntax_list = []
            for f in pkg_resources.resource_listdir(__name__, self.syntax_directory):
                with open(pkg_resources.resource_filename(__name__, self.syntax_directory + "/" + f), 'r') as sf:
                    for syntax_entry in json.load(sf):
                        for from_word in syntax_entry["from"]:
                            self.syntax_list.append({'to': syntax_entry['to'], 'from': from_word})
                        self.syntax_list.append({'to': syntax_entry['to'], 'from': syntax_entry['to']})
        else:
            # should never happen!
            raise Exception("Both syntax_file and syntax_directory are None; cannot load syntax.")

        # make sure that the syntax is correctly formatted
        for syntax_item in self.syntax_list:
            if "to" not in syntax_item or "from" not in syntax_item:
                raise InvalidSynonymStandardizationDictionary("Every element needs to have a to field and a from field")            
        
        # create the syntax_dictionary from saytex to an index in the syntax_list
        self.syntax_dictionary = {}
        for syntax_index, syntax_item in enumerate(self.syntax_list):
            # make sure that there is no command appearing twice
            if syntax_item["from"] in self.syntax_dictionary:
                raise InvalidSynonymStandardizationDictionary("To command appearing twice: " + syntax_item["to"])
            self.syntax_dictionary[syntax_item["from"]] = syntax_index


    def get_standard_synonym(self, word, params = {}):
        """
        Returns the corresponding latex code for saytex, and None if saytex
        is an invalid command. The latex code will be space padded according
        to the value in the dictionary.
        
        :param saytex: str, containing a potential saytex command
        :param params: dict, containing params to be passed to post_process_latex
        
        :return: a post processed str, or None if saytex is not a valid command
        """
        try:
            syntax_entry = self.get_syntax_entry(word)
        except UnrecognizedSynonym:
            return None
        
        return syntax_entry['to']
    
    def get_syntax_entry(self, word):
        """
        Returns a syntax entry corresponding to saytex, if exists.
        Otherwise, raises KeyError.
        
        :param saytex: str, containing a potential saytex command
        
        :return: a dictionary in self.syntax_list
        """
        if word not in self.syntax_dictionary:
            raise UnrecognizedSynonym("The command " + word + " is not recognized.")
        syntax_entry = self.syntax_list[self.syntax_dictionary[word]]
        return syntax_entry
