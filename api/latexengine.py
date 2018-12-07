import re


# constants
from enum import Enum
class Mathwords(Enum):
    INTEGRAL = 'integral'
    SUM = 'sum'

class Controlwords(Enum):
    FROM = 'FROMFROMFROM'
    ENDFROM = 'ENDFROMFROMFROM'
    TO = 'TOTOTO'
    ENDTO = 'ENDTOTOTO'


latexdictionaryfile = 'latexdictionary.txt'
latexdictionary = None
def get_latexdictionary():
    global latexdictionary
    global latexdictionaryfile
    if latexdictionary is not None:
        return latexdictionary
    latexdictionary = {}
    with open(latexdictionaryfile, 'r') as df:
        section = []
        sectionname = ""
        for l in df:
            if l.startswith("SECTION"):
                if len(section) > 0:
                    latexdictionary[sectionname] = section
                section = []
                sectionname = l.split()[1]
                continue
            t = [x.strip() for x in l.split(',')]
            section.append((t[0],t[1]))
        if len(section) > 0:
            latexdictionary[sectionname] = section
    return latexdictionary



def convert_dictionary(s):
    s = makeword(s)
    conversions = []
    for section in get_latexdictionary():
        conversions += get_latexdictionary()[section]
    print(conversions)
    for replacetuple in conversions:
        s = s.replace(makeword(replacetuple[0]), makeword(replacetuple[1]))
    return s.strip()
def makeword(s):
    return ' ' + s + ' '
def makeregexword(s):
    return r'\b' + s + r'\b'




def parse_spoken_numbers(s):
    """
    parameters:
        s: a string containing a math expression

    returns:
        a string where all spoken math numbers are converted into digit form
    """
    # easiest way is probably to enumerate all possible numbers, or maybe not
    digits = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    tons = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    tens = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    
    class numberpart:
        def __init__(self, s, v, p):
            self.s = s
            self.v = v
            self.p = p
        def __str__(self):
            return self.s
    
    ns = []
    for i, d in enumerate(digits):
        ns.append(numberpart(d, i, 0))
    for i, d in enumerate(tons):
        ns.append(numberpart(d, i+10, 1))
    for i, d in enumerate(tens):
        ns.append(numberpart(d, (i+2)*10, 2))
    ns.append(numberpart('hundred',100,3))
    ns.append(numberpart('thousand',1000,4))
    ns.append(numberpart('million',1000000,5))
    ns.append(numberpart('billion',1000000000,6))
    ns.append(numberpart('trillion',1000000000000,7))

    nsdict = {}
    for npart in ns:
        nsdict[str(npart)] = npart

    # now iterate through the string linearly!
    innumber = False
    news = ""
    curnumber = []
    for word in s.split():
        if word == 'and' and innumber:
            continue
        if word in nsdict:
            innumber = True
            b = nsdict[word]
            if len(curnumber) == 0:
                curnumber.append(b.v)
            else:
                if curnumber[-1] > b.v:
                    curnumber.append(b.v)
                else:
                    mult = 0
                    while curnumber[-1] < b.v:
                        mult += curnumber[-1]
                        curnumber.pop()
                        if len(curnumber) == 0:
                            break
                    curnumber.append(mult * b.v)
        else:
            if innumber:
                dnm = 0
                for x in curnumber:
                    dnm += x
                news += " " + str(dnm)
                innumber = False
                curnumber = []

            news += " " + word

    if innumber:
        dnm = 0
        for x in curnumber:
            dnm += x
        news += " " + str(dnm)
        innumber = False

    return news



def find_subscripts(s):
    """
    Find subscripts and replace them.

    A single letter followed by a number is defined as a subscript.

    Also, the word sub is always replaced by a subscript.

    Note that greek letters should also be considered as letters.
    """

    #regular letters
    s = re.sub(r'(\b[a-zA-z]) ([0-9]+)', r'\1_\2', s)
    
    greek_letters = [x[0] for x in get_latexdictionary()['greekletters']]

    s = re.sub(r'\b(' + '|'.join(greek_letters) + ') ([0-9]+)', r'\1_\2', s)

    s = re.sub(r' sub ', r'_', s)

    return s
            



def symbolify_fromtos(s):
    """
    Replaces all from-to-sequences using symbolify_fromto.
    """
    ns = s
    while True:
        try:
            ns = symbolify_fromto(ns)
        except NoFromTo:
            break
    return ns

class NoFromTo(Exception):
    pass

def symbolify_fromto(s):
    """
    Finds a from-to-sequence and its corresponding sum or integral.
    Then concatenates the symbol so as to make it easier to parse.

    We assume that everything between the words "from" and "to" is
    the from part. We assume that the first simple expression after
    "to" is the to part. Simple expression is defined as at most two
    variables and one operation. If parantheses, it uses that.

    In the case where there is no matching "to" word for a "from" word,
    we assume that the entirety of the rest of the string is the from part.

    The return string is formatted as sum FROMFROMFROM expression1 ENDFROMFROMFROM TOTOTO expression2 ENDTOTOTO.
    ('sum' can be substituted for 'integral'.)
    """
    s = makeword(s)
    fromindex = s.find(makeword("from")) + 1
    if fromindex == 0:
        raise NoFromTo
    fromindexend = fromindex + len("from")

    toindex = s[fromindex:].find(makeword("to")) + 1 + fromindex
    if toindex == -1 + 1 + fromindex:
        # no match, set end of string as toindex
        toindex = len(s)
    toindexend = toindex + len("to")

    # determine the endtoindex
    # do this using the following strategy:
    # - if it starts with '(' then find matching ')'
    # otherwise just assume only the next word is part of it
    # except: +, !, ^x (not - because consider sum from 0 to n of minus 1 to the i)
    endtoindex = toindexend
    while endtoindex < len(s):
        tostring = s[endtoindex:]
        tostring = tostring.strip()
        if tostring[0] == '(':
            # find matching
            endparantheses = findmatching(tostring,0)
            if endparantheses > len(tostring):
                # we don't care if the parantheses are matched
                endparantheses = endparantheses - 1
            endtoindex = endparantheses + 1
            break
        else:
            tostringwords = tostring.split()
            if len(tostringwords) > 2:
                if tostringwords[1] == '+':
                    # think about this before changing! remember the continue, which makes sure that everything is included
                    # this is smart code
                    endtoindex = s[endtoindex:].find('+') + endtoindex + 1
                    continue
            if len(tostringwords) > 1:
                if tostringwords[1] == '!':
                    endtoindex = s[endtoindex:].find('!') + 1 + endtoindex
                    break
                if tostringwords[1] == '^':
                    # think about this before changing! remember the continue, which makes sure that everything is included
                    # this is smart code
                    endtoindex = s[endtoindex:].find('^') + endtoindex + 1
                    continue
                if tostringwords[1].startswith('^'):
                    endtoindex = s[endtoindex:].find(tostringwords[1]) + len(tostringwords[1]) + endtoindex
                    break
            endtoindex = s[endtoindex:].find(tostringwords[0]) + len(tostringwords[0]) + endtoindex
            break

    
    # find the closest sum or integral before
    closestsumindex = s[:fromindex].rfind(makeword(Mathwords.SUM.value)) + 1
    closestintegralindex = s[:fromindex].rfind(makeword(Mathwords.INTEGRAL.value)) + 1

    closestindex = closestsumindex
    closestindexend = closestindex + len(Mathwords.SUM.value)
    if closestintegralindex > closestsumindex:
        closestindex = closestintegralindex
        closestindexend = closestindex + len(Mathwords.INTEGRAL.value)

    if closestindex == -1:
        raise NoFromTo


    newstring = s[:closestindexend] + makeword(Controlwords.FROM.value) + s[fromindexend:toindex] + makeword(Controlwords.ENDFROM.value)
    endstring = s[closestindexend:fromindex]
    if toindexend <= len(s):
        newstring += makeword(Controlwords.TO.value) + s[toindexend:endtoindex] + makeword(Controlwords.ENDTO.value)
        endstring += " " + s[endtoindex:]

    newstring = newstring + endstring

    return newstring
    
    


def runengine(s):
    """
    The main method for running the engine converting a math str to a latex str

    parameters:
        s: str of math expression

    returns:
        latex str
    """
    s = makeword(s)
    s = convert_dictionary(s)
    print(s)
    s = parse_spoken_numbers(s)
    print(s)
    s = find_subscripts(s)
    print(s)
    s = symbolify_fromtos(s)
    print(s)
    s = lineareval(s)

    return s.strip()
    

def is_number(s):
    operators=['+', '-', '*', '/', '(', ')','=','^']
    return s not in operators
    '''
        try:
        int(str)
        return True
    except ValueError:
        return False
    '''
 
def is_name(str):
    return re.match(r"\w+", str)
 
def peek(stack):
    return stack[-1] if stack else None
 
def apply_operator(operators, values):
    print(operators)
    print(values)
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    if operator=='/':
        values.append("\\frac{"+str(left)+"}{"+str(right)+"}")
    else:
        values.append("{0}{1}{2}".format(left, operator, right))
 
def greater_precedence(op1, op2):
    precedences = {'=': -1, '+' : 0, '-' : 0, '*' : 1, '/' : 1, '^': 2}
    return precedences[op1] > precedences[op2]
 
def evaluate(expression):
    tokens = re.findall(r"[\^+/*=()-]|\w+", expression)
    print(tokens)
    values = []
    operators = []
    for token in tokens:
        if is_number(token):
            values.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            top = peek(operators)
            while top is not None and top != '(':
                apply_operator(operators, values)
                top = peek(operators)
            operators.pop() # Discard the '('
        else:
            # Operator
            top = peek(operators)
            while top is not None and top not in "()" and greater_precedence(top, token):
                apply_operator(operators, values)
                top = peek(operators)
            operators.append(token)
    while peek(operators) is not None:
        apply_operator(operators, values)

    print(values)
    return values[0]



def findmatching(s,pos):
    """
    Find matching parantheses.

    params:
        s: string, to be searched in
        pos: int, position of ( we want to find a match for

    returns:
        int, position of matching ) bracket
        - if there is no match, return len(s)
    """
    count = 1
    ps = pos + 1
    while count > 0 and ps < len(s):
        if s[ps]=='(':
            count+=1
        if s[ps]==')':
            count-=1
        if count == 0:
            break
        ps += 1
    
    return ps

def lineareval(expression,preans='',prelast='',curx=0):
    ans=preans
    last=prelast
    cur_expr=curx

    expression = expression.lstrip()
    tokens = expression.split(" ")
    print(tokens)

    pos = 0

    for token in tokens:
        dis=token
        addl=True
        pos += len(token)
        if token=="(":
            mmm = findmatching(expression,pos-1)+1
            if mmm > len(expression):
                # if there is no matching parantheses, we don't really care
                mmm -= 1
            print('mmm: ' + str(mmm))
            if addl:
                ans+=last
            if cur_expr==1:
                dis += '}'
            dis = "(" + lineareval(expression[pos:mmm])
            print('expression: ' + expression[mmm:])
            print("preans: " + ans)
            print("prelast: " + dis)
            print("curexpr: " + str(cur_expr))
            if cur_expr==1:
                dis += '}'
            if mmm == len(expression):
                expression += ' '
            return lineareval(expression[mmm:],ans,dis,0)
            
        if token.startswith("^"):
            last += token
            pos +=1
            continue
        if token=="forall":
            dis = "\\forall "
        if token=="<=":
            dis = "\leq "
        if token=='>=':
            dis='\geq '
        if token=='exists':
            dis='\exists '
        if token=='implies':
            dis='\implies '
        if token=='equiv':
            dis='\iff '
        if token=='infinity':
            dis='\infty '
        if token=='then':
            dis='.\:'
        if token==Mathwords.INTEGRAL.value:
            dis='\\int '
        if token==Mathwords.SUM.value:
            dis='\\sum '
        if token==Controlwords.FROM.value:
            dis='_{'
        if token==Controlwords.ENDFROM.value:
            dis='}'
        if token==Controlwords.TO.value:
            dis='^{'
        if token==Controlwords.ENDTO.value:
            dis='}'
        if token=='/':
            dis='\\frac{'+last+'}{'
            addl=False
            cur_expr=2
        if token=='*':
            dis='\cdot '
        if token=='cosine':
            dis='\\cos '
        if token=='sine':
            dis='\\sin '
        if token=='tan':
            dis='\\tan '
        if token=='in':
            dis='\\in '
        if addl:
            ans+=last
        if cur_expr==1:
            dis += '}'
        cur_expr -=1
        cur_expr=max(cur_expr,0)
        last=dis
        pos+=1
    ans+=last
    if cur_expr>0:
        ans+= '}'

    
    ans=ans.replace("cos ^", "cos^")
    ans=ans.replace("sin ^", "sin^")

    return ans
