#!/usr/bin/env python3
import os
from .compiler import SaytexSyntax, SaytexSyntaxError
import unittest
import doctest


class TestToLatex(unittest.TestCase):

    def setUp(self):
        # initialize the compiler
        self.saytex_compiler = SaytexSyntax()
    
    def verify(self, saytex, latex):
        compiler_output = self.saytex_compiler.to_latex(saytex)
        self.assertEqual(latex, compiler_output)
    
    def saytex_exception(self, saytex):
        try:
            self.saytex_compiler.to_latex(saytex)
        except SaytexSyntaxError:
            self.assertTrue(True)
            return
        self.assertFalse(True, "SayTeX should have given exception, but it did not.")

    def test_01(self):
        saytex = "5 plus 3"
        latex = "5 + 3"
        self.verify(saytex, latex)
    
    def test_02(self):
        saytex = "5 plus 3 plus 8"
        latex = "5 + 3 + 8"
        self.verify(saytex, latex)
    
    def test_03(self):
        saytex = "5 plus 3 centered dot 8"
        latex = "5 + 3 \\cdot 8"
        self.verify(saytex, latex)
    
    def test_04(self):
        saytex = "5 plus 3 centered dot 8 superscript 2 plus 2"
        latex = "5 + 3 \\cdot 8^2 + 2"
        self.verify(saytex, latex)
    
    def test_05(self):
        saytex = "3 squar[ed"
        self.saytex_exception(saytex)

    def test_06(self):
        saytex = "integral subscript 0 superscript 10"
        latex = "\\int_0^{10}"
        self.verify(saytex, latex)

    def test_07(self):
        saytex = "integral subscript 0 superscript infinity minus a subscript b"
        latex = "\\int_0^\\infty - a_b"
        self.verify(saytex, latex)
    
    def test_08(self):
        saytex = "integral subscript 0 superscript begin n plus 1 end x dx"
        latex = "\\int_0^{n + 1} x dx"
        self.verify(saytex, latex)
    
    def test_09(self):
        saytex = "fraction begin x end begin y end"
        latex = "\\frac{x}{y}"
        self.verify(saytex, latex)

    def test_10(self):
        saytex = "alpha subscript i plus beta subscript i equals gamma subscript i"
        latex = "\\alpha_i + \\beta_i = \\gamma_i"
        self.verify(saytex, latex)

    def test_11(self):
        saytex = "alpha subscript i plus beta subscript i is less than or equal to gamma subscript i"
        latex = "\\alpha_i + \\beta_i \\leq \\gamma_i"
        self.verify(saytex, latex)
    
    def test_12(self):
        saytex = "alpha subscript i plus beta subscript i is less than gamma subscript i"
        latex = "\\alpha_i + \\beta_i < \\gamma_i"
        self.verify(saytex, latex)
    
    def test_13(self):
        saytex = "p in P implies a does not divide p"
        latex = "p \\in P \\implies a \\nmid p"
        self.verify(saytex, latex)
    
    def test_14(self):
        saytex = "integral subscript 0 superscript 1 sine left parenthesis x plus 1 right parenthesis small space dx equals fraction begin 1 end begin 2 end"
        latex = "\\int_0^1 \\sin \\left( x + 1 \\right) \\, dx = \\frac{1}{2}"
        self.verify(saytex, latex)
    
    def test_15(self):
        saytex = "text begin this is normal text end"
        latex = "text{this is normal text}"
        # NOTE: this is probably not the behavior we want
        self.verify(saytex, latex)



if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
