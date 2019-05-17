#!/usr/bin/env python3

import requests

from flask import *
app = Flask(__name__)
app.config["PREFERRED_URL_SCHEME"] = "https"

from saytex import Saytex, UnrecognizableSaytexInput

saytex_compiler = Saytex()

import config


@app.route("/")
def index():
    return render_template('index.html',    microsoft_authorization_token = get_microsoft_authorization_token(), 
                                            microsoft_region_key = config.MICROSOFT_REGION_KEY, 
                                            api_url = config.API_URL,
                                            css_filename  = config.CSS_FILENAME
    )




def get_microsoft_authorization_token():
    # get a microsoft authorization token
    
    tokenurl = 'https://' + config.MICROSOFT_REGION_KEY + '.api.cognitive.microsoft.com/sts/v1.0/issuetoken'
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': config.MICROSOFT_SPEECH_API_KEY}

    result = requests.post(tokenurl, headers=headers)

    return result.text



@app.route("/api/latex/<string:text>")
def get_latex(text):
    try:
        latex = saytex_compiler.to_latex(text)
    except UnrecognizableSaytexInput:
        latex = r"\text{" + "Unrecognizable Input" + "}"
    except:
        latex = r"\text{Myserious Error}"
        
    return latex

@app.route("/api/saytex/<string:text>")
def get_saytex(text):
    try:
        saytex = saytex_compiler.to_saytex(text)
    except UnrecognizableSaytexInput:
        saytex = r"\text{" + "Unrecognizable Input" + "}"
    except:
        saytex = r"\text{Myserious Error}"
    
    return saytex