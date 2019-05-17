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

        # the implementations works by finding each "over" sequentially
        # for each "over", the find_associativity methods are used to
        # determine where the numerator and denominator begin and end

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
                final_words.insert(-delta_start_index, "fraction")
                if final_words[-delta_start_index] != "begin":
                    final_words.insert(-delta_start_index, "begin")
                    final_words.append('end')
                if index+1 >= len(input_words) or input_words[index+1] != "begin":
                    final_words.append("begin")
                final_words.extend(input_words[index+1:end_index+1])
                if index+1 >= len(input_words) or input_words[index+1] != "begin":
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
        # if last word is "end", then find matching "begin"
        if words[over_index-1] == "end":
            return findmatching(words, over_index-1, w1="begin", w2="end", forward=False)
        
        before_string = " ".join(words[:over_index])
        #print(before_string)
        if before_string.endswith("right parenthesis"):
            # find matching
            startindex = findmatching(words, over_index-1, forward=False)
            # check if the previous word could possible be a function word
            if startindex > 0:
                #print(words[startindex-1])
                if words[startindex-1] not in self.saytex_syntax_operators():
                    startindex = startindex - 1
            
            return startindex
        
        if over_index > 2:
            if words[over_index-2] == 'superscript':
                return self.find_associativity_left(words, over_index-2)

        return over_index - 1
    
    def find_associativity_right(self, words, over_index):
        """
        Finds the index of the end word of the denominator,
        using some heuristic.

        :param words: list of words
        :param over_index: index where the word 'over' is in the words list

        :return: index i such that words[over_index+1:i+1] are the denominator
        """
        if len(words) == over_index+1:
            return over_index
        # if first word is "begin", then find matching "end"
        if words[over_index+1] == "begin":
            return findmatching(words, over_index+1, w1="begin", w2="end", forward=True)
        
        after_string = " ".join(words[over_index+1:])
        if after_string.startswith("left parenthesis"):
            # find matching
            startindex = findmatching(words, over_index+1, forward=True)
            return startindex
        
        if over_index < len(words) -2:
            dafter_string = " ".join(words[over_index+2:])
            if dafter_string.startswith("left parenthesis"):
                # find matching
                startindex = findmatching(words, over_index+2, forward=True)
                return startindex
            if dafter_string.startswith("superscript"):
                return self.find_associativity_right(words, over_index+2)
        
        return over_index + 1
    

def findmatching(words,pos,w1='left parenthesis',w2='right parenthesis',forward=True):
    """
    Find matching parantheses.

    :param words: list, to be searched in
    :param pos: int, position of ( we want to find a match for

    :return: int, position of matching ) bracket; if there is no match, return len(s)
    """

    if forward:

        count = 1
        ps = pos + 1
        while count > 0 and ps < len(words):
            this_string = " ".join(words[ps:])
            if this_string.startswith(w1):
                count+=1
            if this_string.startswith(w2):
                count-=1
            if count == 0:
                break
            ps += 1

        return ps + len(w2.split()) - 1
    
    else:

        count = 1
        ps = pos - 1
        while count > 0 and ps >= 0:
            this_string = " ".join(words[:ps+1])
            if this_string.endswith(w2):
                count+=1
            if this_string.endswith(w1):
                count-=1
            if count == 0:
                break
            ps -= 1

        return ps - len(w1.split()) + 1