# SayTeX
Speak math, get LaTeX!

SayTeX is a tool for converting spoken math into LaTeX equations. Read the documentation at https://saytex.readthedocs.io.

## Structural Overview

As it currently stands, SayTeX consists of three parts operating somewhat independently:

1. **Speech to Text.** In the current implementation, the Microsoft Speech API is used.
2. **Text to SayTeX Syntax.** The SayTeX Syntax is designed to be optimized for speech but still be precise enough for advanced math equations. Currently, the SayTeX Syntax is not very extensive or standardized; work has to be done in that area.
3. **SayTeX Syntax to LaTeX.** This is where most of early development efforts have been concentrated. At the moment, SayTeX uses both the Wolfram Alpha API and a custom-built linear-scan model and lets the user decide which of them produces the best output.

Ideally, part two should not be necessary. However, as long as SayTeX continues to use an external API for part one, it will be; the external API will not necessarily return valid SayTeX Syntax.

## Progress

- [x] Develop a systematic SayTeX Syntax. This is a major and crucial task.
- [ ] Enable users to modify the output and store the modified result, so as to build up a database of correct mappings between speech and LaTeX that can later be used for e.g. machine learning.
- [ ] Use a customized version of the Microsoft Speech API that is adapted to the SayTeX Syntax.
- [ ] Integrate SayTeX with tools that are currently used by visually impaired students, to enable them to more easily typeset math formulas.


## Installation

Install it using PyPI: `pip3 install saytex`.

To install the local version, and keep it updated, use `pip3 install -e .`.

## About

SayTeX is currently developed as a research project by Arvid Lunnemark, under the supervision of Dr. Kyle Keane within the Department of Materials Science in the Interactive Materials Education Laboratory at MIT. The research proposals can be found in the folder `research-proposals`.

All code is open source and licensed under the MIT License. Contributions are welcome.
