"""Server for cafe information app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db

from jinja2 import StrictUndefined

import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """show my homepage"""

    return render_template('homepage.html')

@app.route("/account")
def account():
    """show login and registeration"""

    return render_template('login.html')

@app.route("/login", methods=["POST"])
def login():
    """login to account"""

    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    """register for account"""

    email = request.form.get("register-email")
    password = request.form.get("register-password")

    user = crud.get_user(email)
    if user:
        flash("An account with this email already exists.")
    else:
        crud.create_user(email, password)
        flash ("Your account was created! Log in now.")

    return redirect ("/account")


if __name__ == '__main__':
    connect_to_db(app, "cafes")
    app.run(host='0.0.0.0', debug=True)
