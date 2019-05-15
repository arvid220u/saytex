#!/usr/bin/env python3
import os
import unittest
import doctest

from saytex import Saytex, UnrecognizableSaytexInput

import saytex.layers

class TestSpeechRecognitionErrorDetection(unittest.TestCase):

    def setUp(self):
        self.layer = saytex.layers.SaytexLayer.get_layer("speech_recognition_error_correction")

    def verify(self, inp, oup):
        computed_output = self.layer.execute_layer(inp)
        self.assertEqual(computed_output, oup)
    
    def test_01(self):
        inp = "eggs times why"
        oup = "x times y"
        self.verify(inp, oup)

class TestToLatex(unittest.TestCase):

    def setUp(self):
        # initialize the compiler
        self.saytex_compiler = Saytex()
    
    def verify(self, saytex, latex):
        compiler_output = self.saytex_compiler.to_latex(saytex)
        self.assertEqual(latex, compiler_output)
    
    def saytex_exception(self, saytex):
        try:
            self.saytex_compiler.to_latex(saytex)
        except UnrecognizableSaytexInput:
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
        saytex = "5 plus 3 multiplied by 8"
        latex = "5 + 3 \\cdot 8"
        self.verify(saytex, latex)
    
    def test_04(self):
        saytex = "5 plus 3 multiplied by 8 to the power of 2 plus 2"
        latex = "5 + 3 \\cdot 8^2 + 2"
        self.verify(saytex, latex)
    
    def test_05(self):
        saytex = "3 squar[ed"
        self.saytex_exception(saytex)

    def test_06(self):
        saytex = "integral from 0 to 10"
        latex = "\\int_0^{10}"
        self.verify(saytex, latex)

    def test_07(self):
        saytex = "integral from 0 to infinity minus a subscript b"
        latex = "\\int_0^{\\infty} - a_b"
        self.verify(saytex, latex)
    
    def test_08(self):
        saytex = "integral from 0 to begin n plus 1 end x dx"
        latex = "\\int_0^{n + 1} x dx"
        self.verify(saytex, latex)
    
    def test_09(self):
        saytex = "eggs minus infinity equals 2"
        latex = "x - \\infty = 2"
        self.verify(saytex, latex)

    def test_10(self):
        saytex = "capital a plus b equals five minus capital omega"
        latex = r'A + b = 5 - \Omega'
        self.verify(saytex, latex)
    
    def test_11(self):
        saytex = "integral from 0 to open n plus 1 close x dx"
        latex = "\\int_0^{\\left( n + 1 \\right)} x dx"
        self.verify(saytex, latex)
    
    def test_12(self):
        saytex = "a divided by b"
        latex = r"\frac{a}{b}"
        self.verify(saytex, latex)
    
    def test_13(self):
        saytex = "a plus 1 divided by b"
        latex = r"a + \frac{1}{b}"
        self.verify(saytex, latex)
    
    def test_14(self):
        saytex = "open a plus 1 close over b"
        latex = r"\frac{a + 1}{b}"
        self.verify(saytex, latex)
    
    def test_15(self):
        saytex = "A plus B minus c"
        latex = "a + b - c"
        self.verify(saytex,latex)

    def test_16(self):
        saytex = "f of x equals x squared"
        latex = "f \\left( x \\right) = x^2"
        self.verify(saytex,latex)
    
    def test_17(self):
        saytex = "f of x equals integral of t squared from zero to x dt"
        latex = "f \\left( x \\right) = \\int_0^{x} t^2 dt"
        self.verify(saytex,latex)

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
