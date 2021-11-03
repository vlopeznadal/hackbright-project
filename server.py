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
def account():
    """show login and registeration"""

    return render_template('login.html')

@app.route("/login", methods=["POST"])
def login():
    """login to account"""

    email = request.form.get("login-email")
    password = request.form.get("login-password")

    user = crud.get_user(email)

    if password == user.password:
            session["user"] = user.user_id
    else:
            flash("Incorrect password.")

    return render_template('main.html')


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
        flash("Your account was created! Log in now.")

    return redirect ("/")

@app.route("/cafes", methods=["POST"])
def query():
    """search for cafes"""

    cafes= crud.get_cafes()

    return render_template('results.html', cafes=cafes)

if __name__ == '__main__':
    connect_to_db(app, "cafes")
    app.run(host='0.0.0.0', debug=True)
