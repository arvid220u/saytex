
SYNTAX_DIRECTORY = "saytex_dictionary"
"""
The path to the directory containing all syntax files.
The specifications for the files can be found in saytex-syntax-v01.md.
"""



MAX_WORDS_PER_SAYTEX_COMMAND = 7
"""
This constant should correspond to the most recent definition of the SayTeX Syntax.
Note that the total time of the SayTeX Syntax Compiler will be O(n*m) if m is the variable below,
so be careful. (Also, it will be O(n^2).)
"""



ALLOWED_CHARACTERS_IN_SAYTEX_WORD = set([chr(i) for i in range(ord('a'),ord('z')+1)] + \
                                        [chr(i) for i in range(ord('A'),ord('Z')+1)])
"""
This constant should correspond to the most recent definition of the SayTeX Syntax.
Note that the specification allows for both words and numbers, the latter of which are
not restricted to the characters below.
"""