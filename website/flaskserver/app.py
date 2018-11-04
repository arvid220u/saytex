#!/usr/bin/env python3

from flask import *
app = Flask(__name__)
app.config["PREFERRED_URL_SCHEME"] = "https"



# IMPORTANT THINGS START HERE



from main import text2latex, endtext
@app.route("/api/<string:text>")
def API(text):
    return text2latex(text)

@app.route("/api2/<string:text>")
def API2(text):
    print("api2")
    return endtext(text)

@app.route("/")
def index():
    return render_template("sp.htm")


