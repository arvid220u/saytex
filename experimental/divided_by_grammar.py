#
# This example shows how to write a basic calculator with variables.
#

from lark import Lark, Transformer, v_args


try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass


calc_grammar = ""
with open("divided_by_grammar.lark", 'r') as grammar_file:
    calc_grammar = grammar_file.read()

"""
@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg
    number = float

    def __init__(self):
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def var(self, name):
        return self.vars[name]
"""

calc_parser = Lark(calc_grammar, parser='earley', ambiguity="explicit")#, transformer=CalculateTree())
calc = calc_parser.parse


def main():
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(calc(s))


def test():
    print(calc("sine left parenthesis x right parenthesis over b").pretty())
    print(calc("1+a*-3"))


if __name__ == '__main__':
    test()
    #main()
