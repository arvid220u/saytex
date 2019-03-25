"""
Defines the SaytexSyntax class, containing methods for converting between SayTeX and LaTeX.
"""

import syntax_dictionary
import config


class SaytexSyntaxError(Exception):
    """
    Raised in to_latex, if error.
    """
    pass

class LatexParsingError(Exception):
    """
    Raised in from_latex, if error.
    """
    pass


class SaytexSyntax:
    """
    Contains methods to_latex and from_latex for converting between LaTeX
    and SayTeX syntax. Also supports reloading of the syntax dictionary.
    """

    def __init__(self):
        """
        Initializes SaytexSyntax. Specifically, a syntax dictionary will be loaded.
        """
        # load the syntax dictionary from the SYNTAX_FILE specified in config
        self.load_syntax_dictionary(config.SYNTAX_FILE)


    def load_syntax_dictionary(self, syntax_file):
        """
        Load the syntax dictionary as self.syntax_dictionary.
        """
        self.syntax_dictionary = syntax_dictionary.SyntaxDictionary(syntax_file)


    def to_latex(self, saytex_string, word_list = None, word_index = 0, dp_memo = None):
        """
        Converts SayTeX Syntax into LaTeX code.
        :param saytex_string: A string containing valid SayTeX Syntax code.
        :param word_list (optional): A list of tokenized words derived from saytex_string.
        If word_list is not None, then the saytex_string will be ignored. Is normally only used
        for recursive calls.
        :param word_index: The current index in the word_list that we are at. Used in recursive calls.
        If it is not valid SayTeX Syntax, a SaytexSyntaxError will be raised.
        :param dp_memo: A dictionary mapping indices in the word_list to generated LaTeX strings.
        :return: A string containing a valid translation of the input string into LaTeX (if no exception).
        If word_index > 0, the return value is a tuple (string, value) where value is a measure of
        how good the string is as a LaTeX translation of saytex_string.
        """

        # main idea: iterate recursively, and employ a DP strategy
        # this might be too slow for big strings
        # we're returning a string of length O(saytex_string) for all
        # words in saytex_string. Since strings are copied each time,
        # we are basically in O(n^2) time, if n = len(saytex_string)
        # this is so sad. ah, there is a much better way. never return, just add to dp_memo.
        # this is actually so sad. is there a better way to do this?
        # nah, idk. there are better ways that would only keep track of five strings at a time
        # and automatically change which index we are currently using but that would be so cumbersome
        # and bad.
        # another thing would be to instead of doing dp-matching just do naive back-tracking matching,
        # which might, in hind-sight, be better??
        # anyway, this is definitely fast enough for the time being. 

        # initialize dp_memo
        if dp_memo == None:
            dp_memo = {}

        # if the word_index is in our dp_memo, then return that
        if word_index in dp_memo:
            if type(dp_memo[word_index]) == SaytexSyntaxError:
                raise dp_memo[word_index]
            return dp_memo[word_index]


        # if word_list is None, tokenize the saytex_string
        if word_list == None:
            # split by space
            word_list = saytex_string.split()
            # verify that every word is either a number, or a word using the set of allowed characters
            for word in word_list:
                # numbers are allowed
                try:
                    float(word)
                    continue
                except ValueError:
                    pass
                # words must use allowed characters
                is_allowed = True
                for c in word:
                    if c not in config.ALLOWED_CHARACTERS_IN_SAYTEX_WORD:
                        is_allowed = False
                        break
                if not is_allowed:
                    raise SaytexSyntaxError("Word in SayTeX Syntax using unallowed characters: " + word)
        

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
        for command_length in range(1,config.MAX_WORDS_PER_SAYTEX_COMMAND+1):
            command_index_end = word_index + command_length
            command = " ".join(word_list[word_index:command_index_end])
            latex = self.syntax_dictionary.get_latex(command)
            # if latex is not None, recurse
            if latex != None:
                try:
                    ans = self.to_latex("", word_list=word_list, word_index=command_index_end, dp_memo=dp_memo)
                    # do not increase the value
                    possible_answers.append((latex + ans[0], ans[1]))
                except SaytexSyntaxError:
                    pass
            else:
                # if the length of the command is 1, we could possibly interpret this command as an actual word/number
                # that should just be literally transcribed into latex
                # remember that by the way we deal with spaces, we need to space-pad a word
                # also, we want to increase the value since this is not ideal
                if command_length == 1:
                    word = " " + word_list[word_index] + " "
                    try:
                        ans = self.to_latex("", word_list=word_list, word_index=command_index_end, dp_memo=dp_memo)
                        possible_answers.append((word + ans[0], ans[1] + 1))
                    except SaytexSyntaxError:
                        pass
        
        if len(possible_answers) == 0:
            # we found no possible translations of this string into latex
            # this should never happen, since we can just keep adding regular words instead
            raise SaytexSyntaxError("If you get this error, something is deeply wrong with this code.")
        
        # now, return the answer with the minimal value
        chosen_answer = possible_answers[0]
        for a in possible_answers[1:]:
            if a[1] < chosen_answer[1]:
                chosen_answer = a
        
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
        # remember that 2 spaces indicate that both words want space around them
        # and 1 space indicate that 1 of the words do not want space around them
        # that is, >= 2 spaces should be turned into 1 space, and 1 space should be eliminated
        final_latex_string = ""
        space_count = 0
        for c in chosen_latex_string:
            if c == " ":
                space_count += 1
                continue
            if space_count > 1:
                # add a space
                final_latex_string += " "
            space_count = 0
            final_latex_string += c
    
        # return the string
        return final_latex_string



                


        