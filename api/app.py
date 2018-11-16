#!/usr/bin/env python3

from flask import *
app = Flask(__name__)
app.config["PREFERRED_URL_SCHEME"] = "https"

from crossdomain import crossdomain

from flask import Response

import latexconversion



@app.route("/full/<string:text>")
@crossdomain(origin='*')
def fullapi(text):
    """
    converts string to latex using wolfram API
    if an error is returned, the fastapi is used as a fallback

    parameters:
        text: the spoken string to be converted into latex code

    returns:
        latex code
    """
    try:
        latex = latexconversion.wolframlatex(text)
    except:
        latex = latexconversion.simplelatex(text)
    return latex




@app.route("/fast/<string:text>")
@crossdomain(origin='*')
def fastapi(text):
    """
    converts string to latex using fast methods (no external APIs)
    if string cannot be parsed, it returns an error

    parameters:
        text: the spoken string to be converted into latex code

    returns:
        latex code
    """

    #try:
    # convert using simple method
    latex = latexconversion.simplelatex(text)
    """except:
        # return an error
        return Response('String could not be converted into LaTeX.', status=400)"""

    return latex

