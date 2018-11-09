
import requests
import urllib

from shuntington import evaluate
from shuntington import lineareval

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
        ('zero','0'),
        ('one','1'),
        ('two','2'),
        ('three','3'),
        ('four','4'),
        ('five','5'),
        ('six','6'),
        ('seven','7'),
        ('eight','8'),
        ('nine','9'),
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
]

# not used for wolfram alpha, but used for fast API
math_symbols_aggressive = [
        ('by', '*'),
        ('alpha','\\alpha'),
        ('beta','\\beta'),
        ('gamma','\\gamma'),
        ('zeta','\\zeta'),
        ('eta','\\eta'),
        ('theta','\\theta'),
        ('iota','\\iota'),
        ('kappa','\\kappa'),
        ('lambda','\\lambda'),
        ('mu','\\mu'),
        ('nu','\\nu'),
        ('xi','\\xi'),
        ('pi','\\pi'),
        ('rho','\\rho'),
        ('tau','\\tau'),
        ('upsilon','\\upsilon'),
        ('phi','\\phi'),
        ('chi','\\chi'),
        ('psi','\\psi'),
        ('omega','\\omega'),
]

# not used for wolfram alpha, but used for fast API
common_mischaracterizations_aggressive = [
        ('is',' '),
        ('the',' '),
        ('of',' '),
        ('and','n'),
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
]

# used for all APIs
uppercase_to_lowercase = [(x,x.lower()) for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']


def wolframlatex(text):
    text=text.lower().replace('some', 'sum')
    print(text)
    text=replace_symbols(text)
    print(text)
    

    r = requests.get('https://www.wolframcloud.com/objects/arvid/latexdictation/stringtolatex?x=' + urllib.parse.quote_plus(text))
    return r.text


def simplelatex(text):
    """
    convert text to latex using fast method (no external API)

    parameters:
        text: unprocessed spoken string

    returns:
        latex string
    """

    # preprocess string
    preprocessed = preprocess(text)

    # aggressively preprocess
    preprocessed = aggressive_preprocess(preprocessed)

    # do the lineareval
    latex = lineareval(preprocessed)

    # determine if latex is well-formed latex
    # huh

    return latex


# helper methods
def makeword(s):
    return ' ' + s + ' '
def replacelist(s, l):
    for replacetuple in l:
        s = s.replace(makeword(replacetuple[0]), makeword(replacetuple[1]))
    return s

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
    processedtext = makeword(text)
    processedtext = replacelist(processedtext, common_mischaracterizations)
    processedtext = replacelist(processedtext, uppercase_to_lowercase)
    processedtext = replacelist(processedtext, special_vocabulary)
    processedtext = replacelist(processedtext, math_symbols)
    
    return processedtext.strip()

def aggressive_preprocess(text):
    """
    used together with preprocess
    used for the simplelatex conversion

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
