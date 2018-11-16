import re

latexsymbols = [
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

def is_number(str):
    operators=['+', '-', '*', '/', '(', ')','=','^']
    return str not in operators
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
