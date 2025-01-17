from functools import wraps
from flask import session, redirect

def loginRequired(function):
    @wraps(function)
    def decoratedFunction():
        if "username" not in session:
            return redirect("/login")  # Authorization required
        else:
            return function()

    return decoratedFunction

def newUserRequired(function):
    @wraps(function)
    def decoratedFunction():
        if "username" not in session:
            return function()
        else:
            return redirect("/")