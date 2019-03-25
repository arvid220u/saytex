A SayTeX command consists of at most 5 space-separated words.

All words are either numbers, or words using the letters a-z and A-Z.

The specific commands of SayTeX Syntax are specified in json format in
multiple files in `saytexsyntax/saytex_dictionary`. The different json files will
be concatenated by the compiler, and the reason for having multiple ones is purely
organizational.

Each of the json files must be
a list of dictionaries, where each dictionary contains the following elements:
- `saytex`: a string of the saytex command. Required.
- `latex`: a string of the corresponding latex command. Required.
- `left_space`: an integer indicating space preference. If 0, a space should not
be added to its left side, if 1, a space should occasionally be added, and if 2, a space
should always be added. Optional; defaults to 1.
- `right_space`: an integer indicating space preference. Same format as `left_space`.
- `insert_curly_brackets_right`: a boolean indicating whether or not the command (operator)
should require the word on its right to be encapsulated in curly braces (used by e.g. `^`).
Optional; default to `false`.