"""Server for cafe information app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, Favorites, Reviews, db
from jinja2 import StrictUndefined
from datetime import datetime
import crud, cloudinary.uploader, os

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUDINARY_NAME = "damecgv2h"

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

    cafe_id = crud.get_google_cafe()
    google_cafe = crud.get_google_cafe_info(cafe_id)

    user = crud.get_user_by_id(session['user'])
    profile_pic = crud.get_user_image(user)

    if Reviews.query.filter(Reviews.user_id==session["user"], Reviews.cafe_id==session["cafe_id"]).first():
        user_review = True
    else:
        user_review = False
    
    return render_template("details.html", cafe=cafe, review=reviews, review_dates=review_dates, hours=hours, google_cafe=google_cafe, user_review=user_review, profile_pic=profile_pic)

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

    user_reviews = crud.get_user_reviews()

    profile_pic = crud.get_user_image(user)

    return render_template("profile.html", user=user, favorite_cafes=favorite_cafes, user_reviews=user_reviews, profile_pic=profile_pic)

@app.route("/user-image", methods=["POST"])
def upload_user_image():

    user_image = request.files['profile-pic']

    result = cloudinary.uploader.upload(user_image, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUDINARY_NAME)

    img_url = result['secure_url']

    user = crud.get_user_by_id(session['user'])

    user.user_image = img_url
    db.session.commit()

    return ""

@app.route("/profile-pic", methods=["POST"])
def get_profile_pic():

    user = crud.get_user_by_id(session['user'])

    img_url = user.user_image

    if img_url:
        return img_url
    else:
        return "False"
    

@app.route("/coordinates")
def retrieve_coordinates():
    cafes = crud.get_cafes_with_session()
    coordinates = crud.get_cafe_coordinates(cafes)

    return coordinates

@app.route("/coordinate")
def retrieve_coordinate():
    cafe = crud.get_cafe_by_id(session["cafe_id"])
    coordinate = {'latitude' : cafe['coordinates']['latitude'], 'longitude': cafe['coordinates']['longitude']}

    return coordinate

@app.route("/markers")
def retrieve_marker_info():
    cafes = crud.get_cafes_with_session()
    marker_info = crud.get_marker_info(cafes)

    return marker_info

@app.route("/marker")
def retrieve_marker_info_single():
    cafe = crud.get_cafe_by_id(session["cafe_id"])
    cafe_info = {'0': [cafe["name"], cafe["id"], cafe["location"]["address1"], cafe["location"]["city"], cafe["location"]["state"], cafe["location"]["zip_code"]]}

    return cafe_info

@app.route("/ratings")
def retrieve_cafe_ratings():

    yelp = crud.get_cafe_by_id(session["cafe_id"])

    google_id = crud.get_google_cafe()

    google = crud.get_google_cafe_info(google_id)

    yelp_rating = yelp["rating"]

    google_rating = google["rating"]

    return {'yelp': yelp_rating, 'google' : google_rating}

@app.route("/reviews", methods=['POST'])
def retrieve_reviews():
    """get cafe review"""

    if Reviews.query.filter(Reviews.user_id==session["user"], Reviews.cafe_id==session["cafe_id"]).first():
        review = Reviews.query.filter(Reviews.user_id==session["user"], Reviews.cafe_id==session["cafe_id"]).first()
        return jsonify({'date': review.date.strftime('%-m/%-d/%y %-I:%M %p'), 'rating': review.rating, 'review': review.review})
    else:
        return "False"

@app.route("/reviewing", methods=['POST'])
def review():
    """review a cafe"""

    rating = request.form.get("rating")
    text = request.form.get("review")

    date = datetime.now()

    review = Reviews(user_id=session["user"], cafe_id=session["cafe_id"], date=date, rating=rating, review=text)
    db.session.add(review)
    db.session.commit()

    return jsonify({'date': review.date.strftime('%-m/%-d/%y %-I:%M %p'), 'rating': rating, 'review': text})

@app.route("/updating", methods=['POST'])
def review_edit():
    """edit a cafe review"""

    updated_rating = request.form.get("updatedrating")
    updated_text = request.form.get("updatedreview")

    updated_date = datetime.now()

    review = Reviews.query.filter(Reviews.user_id==session["user"], Reviews.cafe_id==session["cafe_id"]).first()
    review.date = updated_date
    review.rating = updated_rating
    review.review = updated_text
    db.session.commit()

    return jsonify({'date': review.date.strftime('%-m/%-d/%y %-I:%M %p'), 'rating': updated_rating, 'review': updated_text})

if __name__ == '__main__':
    connect_to_db(app, "cafes")
    app.run(host='0.0.0.0', debug=True)
