"""
Recognizes from-to sequences such as "integral from ... to ..."
and "sum from ... to ...".
"""

from .layer import SaytexLayer

import re

class NoFromTo(Exception):
    """
    Raised if there is no from-to sequence in a string.
    """
    pass

class FromToRecognitionLayer(SaytexLayer):

    def execute_layer(self, input_string):
        """
        Replaces "from ... to ..." with "subscript begin ... end superscript begin .. end"
        """
        in_progress_string = input_string

        while True:
            try:
                in_progress_string = self.symbolify_fromto(in_progress_string)
            except NoFromTo:
                break
        
        return in_progress_string


    def symbolify_fromto(self, s):
        """
        Finds a from-to-sequence and its corresponding sum or integral.
        We assume that everything between the words "from" and "to" is
        the from part. We assume that the first simple expression after
        "to" is the to part. Simple expression is defined as at most two
        variables and one operation. If parantheses, it uses that.
        In the case where there is no matching "to" word for a "from" word,
        we assume that the entirety of the rest of the string is the from part.
        The return string is formatted as sum subscript begin expression1 end superscript begin expression2 end.
        ('sum' can be substituted for 'integral'.)
        """
        s = makeword(s)
        fromindex = s.find(makeword("from")) + 1
        if fromindex == 0:
            raise NoFromTo
        fromindexend = fromindex + len("from")

        # note, the +1 comes from the makeword
        toindex = s[fromindex:].find(makeword("to")) + 1 + fromindex
        if toindex == -1 + 1 + fromindex:
            # no match, set end of string as toindex
            toindex = len(s)

        toindexend = toindex + len("to")

        # if there is a 'from' between the fromindexend and the toindex,
        # or if the toindex is the len(s)
        # then check if the closest 2 was misheard
        if toindex == len(s) or 'from' in s[fromindexend:toindex]:
            # note, the +1 comes from the makeword
            twoindex = s[fromindex:].find(makeword("2")) + 1 + fromindex
            if twoindex != -1 + 1 + fromindex:
                if twoindex < toindex:
                    oldtoindex = toindex

                    # update the toindex
                    toindex = twoindex
                    toindexend = toindex + len('2')

                    # special case: if the from string becomes empty now, or ends with an equal sign,
                    # interpret it as a 2 still, and try to find the next 2
                    newfromstring = s[fromindexend:twoindex].strip()
                    if newfromstring == '' or newfromstring[-1] == '=':
                        # try to find next 2
                        nexttwoindex = s[twoindex+1:].find(makeword("2")) + 1 + (twoindex+1)
                        if nexttwoindex != -1 + 1 + (twoindex+1) and nexttwoindex < oldtoindex:
                            # use it!
                            toindex = nexttwoindex
                            toindexend = nexttwoindex + len("2")
                        


        # determine the endtoindex
        # do this using the following strategy:
        # - if it starts with '(' then find matching ')'
        # otherwise just assume only the next word is part of it
        # except: +, !, ^x (not - because consider sum from 0 to n of minus 1 to the i)
        endtoindex = toindexend
        dontaddtoseparators = False
        while endtoindex < len(s):
            tostring = s[endtoindex:]
            tostring = tostring.strip()
            if tostring.startswith('left parenthesis'):
                # find matching
                endparantheses = findmatching(tostring,0)
                if endparantheses > len(tostring):
                    # we don't care if the parantheses are matched
                    endparantheses = endparantheses - 1
                endtoindex += endparantheses + len('right parenthesis') + 1
                break
            elif tostring.startswith('begin'):
                endparantheses = findmatching(tostring,0,w1='begin',w2='end')
                if endparantheses > len(tostring):
                    # we don't care if the parantheses are matched
                    endparantheses = endparantheses - 1
                endtoindex += endparantheses + 1 + len('end')
                dontaddtoseparators = True
                break
            else:
                tostringwords = tostring.split()
                if len(tostringwords) > 2:
                    if tostringwords[1] == 'plus':
                        # think about this before changing! remember the continue, which makes sure that everything is included
                        # this is smart code
                        endtoindex = s[endtoindex:].find('plus') + endtoindex + 1
                        continue
                if len(tostringwords) > 1:
                    if tostringwords[1] == 'factorial':
                        endtoindex = s[endtoindex:].find('factorial') + 1 + endtoindex
                        break
                    if tostringwords[1] == 'superscript':
                        # think about this before changing! remember the continue, which makes sure that everything is included
                        # this is smart code
                        endtoindex = s[endtoindex:].find('superscript') + endtoindex + 1
                        continue
                    if tostringwords[1].startswith('superscript'):
                        endtoindex = s[endtoindex:].find(tostringwords[1]) + len(tostringwords[1]) + endtoindex
                        break
                if len(tostringwords) > 0:
                    endtoindex = s[endtoindex:].find(tostringwords[0]) + len(tostringwords[0]) + endtoindex
                break

        
        # find the closest sum or integral before
        closestsumindex = s[:fromindex].rfind(makeword("sum")) + 1
        closestintegralindex = s[:fromindex].rfind(makeword("integral")) + 1

        closestindex = closestsumindex
        closestindexend = closestindex + len("sum")
        if closestintegralindex > closestsumindex:
            closestindex = closestintegralindex
            closestindexend = closestindex + len("integral")

        if closestindex == -1:
            raise NoFromTo

        frombeginword = "subscript begin"
        fromendword = "end"
        if len(s[fromindexend:toindex].strip()) == 1:
            frombeginword = "subscript"
            fromendword = ""
        

        newstring = s[:closestindexend] + makeword(frombeginword) + s[fromindexend:toindex] + makeword(fromendword)
        endstring = s[closestindexend:fromindex]
        if toindexend <= len(s):
            if not dontaddtoseparators:
                newstring += makeword("superscript begin") + s[toindexend:endtoindex] + makeword("end")
            else:
                newstring += makeword("superscript") + s[toindexend:endtoindex]
            endstring += " " + s[endtoindex:]

        newstring = newstring + endstring

        newstring = " ".join([x for x in newstring.split(" ") if x != ""])

        return newstring

def makeword(s):
    return ' ' + s + ' '

def findmatching(s,pos,w1='left parenthesis',w2='right parenthesis'):
    """
    Find matching parantheses.
    
    :param s: string, to be searched in
    :param pos: int, position of ( we want to find a match for
    
    :return: int, position of matching ) bracket; if there is no match, return len(s)
    """
    count = 1
    ps = pos + 1
    while count > 0 and ps < len(s):
        if s[ps:].startswith(w1):
            count+=1
        if s[ps:].startswith(w2):
            count-=1
        if count == 0:
            break
        ps += 1
    
    return ps