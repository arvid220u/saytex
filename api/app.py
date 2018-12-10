#!/usr/bin/env python3


from flask import *
app = Flask(__name__)
app.config["PREFERRED_URL_SCHEME"] = "https"

from crossdomain import crossdomain

from flask import Response

import latexconversion

import re



@app.before_first_request
def logging_init():
    import logging
    logging.basicConfig(level=logging.DEBUG)



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

    # split the text at equals
    # maybe introduce caching here at some point, so that all wolfram expressions don't need to be re-evaluated?
    # smart splitting needs to be done. for example, if the equals sign is after a 'from' then don't split

    expressions = filter(None, re.split(r'(?<!from [^\s] )(equals|is equal to)', text))
    
    finallatex = ""

    for expression in expressions:
        
        try:
            latex = latexconversion.wolframlatex(expression)
        except latexconversion.WolframError:
            latex = latexconversion.simplelatex(expression)

        if finallatex != "":
            finallatex += " = "

        finallatex += latex


    return finallatex




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

