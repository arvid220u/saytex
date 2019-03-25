"""
The path to the syntax file.
The syntax file must be in json format, being an array in which
every element has at least two fields: "saytex" representing the
SayTeX Syntax command, and "latex" representing the corresponding
LaTeX command or symbol. Additionally, there are two optional fields:
"left_space" and "right_space" which are integers indicating spacing
preferences for the command. Normally, these values are either 0 or 1;
0 indicating no space, and 1 indicating a space. If no value is provided,
the command is assumed to have a space preference of 1 in both directions.
"""
SYNTAX_FILE = "saytex_dictionary.json"


"""
This constant should correspond to the most recent definition of the SayTeX Syntax.
Note that the total time of the SayTeX Compiler will be O(n*m) if m is the variable below,
so be careful. (Also, it will be O(n^2).)
"""
MAX_WORDS_PER_SAYTEX_COMMAND = 5


"""
This constant should correspond to the most recent definition of the SayTeX Syntax.
Note that the specification allows for both words and numbers, the latter of which are
not restricted to the characters below.
"""
ALLOWED_CHARACTERS_IN_SAYTEX_WORD = set([chr(i) for i in range(ord('a'),ord('z')+1)] + \
                                        [chr(i) for i in range(ord('A'),ord('Z')+1)])