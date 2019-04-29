"""
The saytex package mainly consists of the Saytex class, used for
converting from natural language to LaTeX, as well as the SaytexSyntax
class, used for converting from the intermediary SayTeX Syntax into
LaTeX.
"""

# import the core functionality
from .compiler import Saytex, UnrecognizableSaytexInput

# also import the saytex syntax
from .saytexsyntax import SaytexSyntax, SaytexSyntaxError

