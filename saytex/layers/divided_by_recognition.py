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

        # simple implementation: just take previous word.

        input_words = input_string.split()

        final_words = []

        index = 0
        while index < len(input_words):
            word = input_words[index]
            if word == 'over' and index > 0:
                start_index = self.find_associativity_left(input_words, index)
                end_index = self.find_associativity_right(input_words, index)
                # insert fraction begin
                delta_start_index = index - start_index
                final_words.insert(-delta_start_index, "fraction begin")
                final_words.append("end begin")
                final_words.extend(input_words[index+1:end_index+1])
                final_words.append('end')
                index = end_index + 1
            else:
                final_words.append(word)
                index += 1

        final_string = " ".join(final_words)

        return final_string
    

    def find_associativity_left(self, words, over_index):
        """
        Finds the index of the start word of the numerator,
        using some heuristic.

        :param words: list of words
        :param over_index: index where the word 'over' is in the words list

        :return: index i such that words[i:over_index] are the numerator
        """
        # for now, just use previous word
        return over_index - 1
    
    def find_associativity_right(self, words, over_index):
        """
        Finds the index of the end word of the denominator,
        using some heuristic.

        :param words: list of words
        :param over_index: index where the word 'over' is in the words list

        :return: index i such that words[over_index+1:i+1] are the denominator
        """
        # for now, just use the next word
        return over_index + 1