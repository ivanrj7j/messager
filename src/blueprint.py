from flask import Blueprint
from flask import render_template

main = Blueprint("mani", __name__)

@main.route("/")
def home():
    return render_template("index.html")