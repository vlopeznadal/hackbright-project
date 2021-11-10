"""Server for cafe information app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, Favorites, db

from jinja2 import StrictUndefined

import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def account():
    """show login and registeration"""
    login=False
    if 'user' in session:
        login=True

    return render_template('homepage.html', login=login)

@app.route("/login", methods=["POST"])
def login():
    """login to account"""

    email = request.form.get("login-email")
    password = request.form.get("login-password")

    user = crud.get_user(email)

    if user == None:
        flash("Account does not exist. Registration required.")
    elif password == user.password:
        session["user"] = user.user_id
    else:
        flash("Incorrect password.")

    return redirect("/")

@app.route("/logout")
def logout():
    session.pop('user', None)
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
        flash("Your account was created! Log in now.")

    return redirect ("/")

@app.route("/cafes", methods=["POST"])
def query():
    """search for cafes"""

    cafes = crud.get_cafes()

    coordinates = []

    for cafe in cafes:
        coordinates.append(cafe["coordinates"])

    if cafes == "error":
        flash("Please input a valid zipcode.")
        return redirect("/")

    return render_template('results.html', cafes=cafes, coordinates=coordinates)
    

@app.route("/cafes/<cafe_id>")
def show_specific_cafe(cafe_id):
    """show the cafe details page"""
    cafe = crud.get_cafe_by_id(cafe_id)

    print(cafe)

    hours = crud.get_cafe_hours(cafe)

    reviews= crud.get_cafe_reviews(cafe_id)

    review_dates=crud.get_review_dates(reviews)

    session["cafe_id"] = cafe_id
    session["cafe_name"] = cafe["name"]
    session["image_url"] = cafe["image_url"]
    session["cafe_street"] = cafe["location"]["address1"]
    session["cafe_city"] = cafe["location"]["city"]
    session["cafe_state"] = cafe["location"]["state"]
    session["cafe_zip"] = cafe["location"]["zip_code"]
    
    return render_template("details.html", cafe=cafe, review=reviews, review_dates=review_dates, hours=hours)

@app.route("/favorite")
def favorite():
    favorite = Favorites(user_id=session["user"], cafe_id=session["cafe_id"], cafe_name=session["cafe_name"], image_url=session["image_url"], cafe_street=session["cafe_street"], 
    cafe_city=session["cafe_city"], cafe_state=session["cafe_state"], cafe_zip=session["cafe_zip"])
    db.session.add(favorite)
    db.session.commit()
    return " "

@app.route("/unfavorite")
def unfavorite():
    unfavorite = Favorites.query.filter_by(cafe_id=session["cafe_id"]).one()
    db.session.delete(unfavorite)
    db.session.commit()
    return " "

@app.route("/database")
def check_database():
    check = Favorites.query.filter((Favorites.cafe_id==session["cafe_id"]) & (Favorites.user_id==session["user"])).first()
    if check is not None:
        return "bi-heart-fill"
    else:
        return "bi-heart"

@app.route("/user/<user_id>")
def show_user_profile(user_id):
    user = crud.get_user_by_id(user_id)

    favorite_cafes = crud.get_user_favorites(user_id)

    return render_template("profile.html", user=user, favorite_cafes=favorite_cafes)

@app.route("/coordinates")
def retrieve_coordinates():
    cafes = crud.get_cafes_with_session()
    coordinates = crud.get_cafe_coordinates(cafes)

    return coordinates

@app.route("/markers")
def retrieve_marker_info():
    cafes = crud.get_cafes_with_session()
    marker_info = crud.get_marker_info(cafes)

    return marker_info


if __name__ == '__main__':
    connect_to_db(app, "cafes")
    app.run(host='0.0.0.0', debug=True)
