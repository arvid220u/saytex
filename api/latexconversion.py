
import requests
import urllib
import re

import latexengine

# used in all APIs
special_vocabulary = [
        ('open', '('),
        ('close', ')')
]

# used in all APIs
math_symbols = [
        ('plus', '+'),
        ('minus', '-'),
        ('over', '/'),
        ('divided by', '/'),
        ('times', '*'),
        ('equals','='),
        ('squared','^2'),
        ('cubed','^3'),
        ('greater than','>'),
        ('less than','<'),
        ('< or equal to','<='),
        ('> or equal to','>='),
]

# used in all APIs
common_mischaracterizations = [
        ('see','c'),
        ('some','sum'), # dubious
        ('end','n'),
        ('hey','a'),
        ('day','a'),
        ('be','b'),
        ('overbyte','over b'),
        ('richer','greater'),
        ("I'm",'n'),
        ('clothes','close'),
        ('whole','close'),
        ('closed','close'),
        ('cosign','cosine'),
        ('quotes','close'),
        ('oakland','open'),
        ('eggs','x'),
        ('clubs','close'),
        ('eclipse','a plus'),
        ('aid','a'),
        ('beat','b'),
        ('nfinity','infinity'),
]

# not used for wolfram alpha, but used for fast API
math_symbols_aggressive = [
        ('by', '*'),
]

# not used for wolfram alpha, but used for fast API
common_mischaracterizations_aggressive = [
        ('is',' '),
        ('the',' '),
        ('of',' '),
        ('sign','sine'),
        ('such that','then'),
        ('we get','then'),
        ('dan','then'),
        ('done','then'),
        ('there exists','exists'),
        ('there exist','exists'),
        ('equivalent to','equiv'),
        ('equal to','equals'),
        ('for all','forall'),
        ('frale','forall'),
        ('integrate','integral'),
]

class WolframError(Exception):
    pass

def wolframlatex(text):
    """
    convert text to latex using wolfram API

    parameters:
        text: unprocessed spoken string

    returns:
        latex string
    """
    preprocessed = preprocess(text)

    print(preprocessed)

    r = requests.get('https://www.wolframcloud.com/objects/arvid/latexdictation/stringtolatex?x=' + urllib.parse.quote_plus(preprocessed))
    latex = r.text

    print(latex)

    # clean up the result
    latex = latex.strip('"')

    # replace escaped backslashes with real ones
    latex = latex.replace('\\\\', '\\')

    # remove starting and ending brackets
    #latex = latex.lstrip('\\[').rstrip('\\]')
    if latex.startswith('\\['):
        latex = latex[2:]
    if latex.endswith('\\]'):
        latex = latex[:-2]
    latex = latex.lstrip('[').rstrip(']')
    
    if '$Failed' in latex:
        raise WolframError

    return latex



def simplelatex(text):
    """
    convert text to latex using fast method (no external API)

    parameters:
        text: unprocessed spoken string

    returns:
        latex string
    """

    # aggressively preprocess
    preprocessed = aggressive_preprocess(text)

    # preprocess string
    preprocessed = preprocess(preprocessed)

    # aggressively preprocess
    preprocessed = aggressive_preprocess(preprocessed)

    # do the lineareval
    latex = latexengine.runengine(preprocessed)

    # determine if latex is well-formed latex
    # huh
    # could check for occurrence of long word, for example

    return latex


# helper methods
def makeword(s):
    return ' ' + s + ' '
def replacelist(s, l):
    for replacetuple in l:
        s = s.replace(makeword(replacetuple[0]), makeword(replacetuple[1]))
    return s

def transformcapitals(text):
    # for every string capital letter, replace with Letter
    # include greek letters!
    return re.sub(r'capital (\D)', lambda x : x.group(1).upper(), text)



def preprocess(text):
    """
    replaces common mischaracterized words (eggs -> x)
    replaces simple math words (over -> divided by)

    parameters:
        text: unprocessed string of spoken math

    returns:
        string
    """
    # replace symbols!
    # order: mischaracterizations, uppercase to lowercase, vocabulary, math symbols

    # convert from lowercase to uppercase
    processedtext = text.lower()

    # make word, to add padding and make edge cases into non-edge cases
    processedtext = makeword(processedtext)

    # turn capital [letter] into [Letter]
    processedtext = transformcapitals(processedtext)

    # replace various things
    processedtext = replacelist(processedtext, common_mischaracterizations)
    processedtext = replacelist(processedtext, special_vocabulary)
    processedtext = replacelist(processedtext, math_symbols)
    
    return processedtext.strip()

def aggressive_preprocess(text):
    """
    used together with preprocess
    used for the simplelatex conversion
    produces a string that is NOT tailored to latex

    parameters:
        text: preprocessed string of spoken math

    returns:
        string
    """
    # replace symbols!
    # order: mischaracterizations, math symbols
    processedtext = makeword(text)
    processedtext = replacelist(processedtext, common_mischaracterizations_aggressive)
    processedtext = replacelist(processedtext, math_symbols_aggressive)
    
    return processedtext.strip()
