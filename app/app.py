#!/usr/bin/env python3

from flask import *
app = Flask(__name__)
app.config["PREFERRED_URL_SCHEME"] = "https"

import config


@app.route("/")
def index():
    return render_template('index.html', microsoft_speech_api_key = config.MICROSOFT_SPEECH_API_KEY, api_url = config.API_URL)
