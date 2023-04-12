from flask import render_template
from camo_code import app, db


@app.route("/")
def home():
    return render_template("home.html")
