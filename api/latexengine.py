import re

latexdictionary = 'latexdictionary.txt'

def convert_dictionary(s):
    s = makeword(s)
    conversions = []
    with open(latexdictionary, 'r') as df:
        for l in df:
            t = [x.strip() for x in l.split(',')]
            conversions.append((t[0],t[1]))
    print(conversions)
    for replacetuple in conversions:
        s = s.replace(makeword(replacetuple[0]), makeword(replacetuple[1]))
    return s.strip()
def makeword(s):
    return ' ' + s + ' '

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
            else:
                news += " " + word

    if innumber:
        dnm = 0
        for x in curnumber:
            dnm += x
        news += " " + str(dnm)
        innumber = False

    return news


            




def runengine(s):
    """
    The main method for running the engine converting a math str to a latex str

    parameters:
        s: str of math expression

    returns:
        latex str
    """
    s = convert_dictionary(s)
    s = lineareval(s)

    return s
    

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
    return re.match("\w+", str)
 
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
    tokens = re.findall("[\^+/*=()-]|\w+", expression)
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



def findmatching(xp,pos):
    count=1
    ps = pos+1
    while count > 0 and ps < len(xp):
        if xp[ps]=='(':
            count+=1
        if xp[ps]==')':
            count-=1
        ps +=1
    
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
            mmm = findmatching(expression,pos-1)
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
        if token=='integral':
            dis='\int '
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
        if token=='sum':
            dis='\\sum '
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
