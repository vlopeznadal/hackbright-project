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
def homepage():
    """View homepage"""

    # if user is logged in, main page with search feature will be displayed
    # otherwise, login and registration forms are shown and required

    # "login" passed into homepage.html to determine what to display on page
    login=False
    if 'user' in session:
        login=True

    return render_template('homepage.html', login=login)


""" ** Routes related login system ** """

@app.route("/login", methods=["POST"])
def login():
    """Use the user's provided email and password to login them in.
    Displays error message if user does not exist or if password is incorrect.
    Saves user's ID in session when logged in successfully.
    Redirects user to homepage where search feature will be displayed."""

    # Grabbing entered in email and password
    email = request.form.get("login-email")
    password = request.form.get("login-password")

    # Checks to see if their is a user in DB with provided email
    user = crud.get_user(email)

    # User does not exist
    if user == None:
        flash("Account does not exist. Registration required.")
    # Password is correct
    elif password == user.password:
        # Save user ID in session
        session["user"] = user.user_id
    # Password is incorrect
    else:
        flash("Incorrect password.")

    # Sends user back to homepage to now use web app
    return redirect("/")

@app.route("/register", methods=["POST"])
def create_account():
    """Use the user's provided email and password to create an account.
    Displays error message if user already exists or if email or password not provided.
    If user does not already exist, details get saved into database and a success message is displayed.
    Redirects user to homepage where they can now login to their account."""

    # Grabbing entered in email and password
    email = request.form.get("register-email")
    password = request.form.get("register-password")

    # Checks to see if their is already a user in DB with provided email
    user = crud.get_user(email)

    # Ensures an email and password is provided
    if not email or not password:
        flash("An email and password required for registration.")
        return redirect(request.referrer)

    # User already exists
    if user:
        flash("An account with this email already exists.")
        return redirect(request.referrer)
    # User doesn't exist
    else:
        # Enters information into DB
        crud.create_user(email, password)
        flash("Your account was created! Log in now.")

    # Sends user back to homepage to login to account
    return redirect ("/")

@app.route("/logout")
def logout():
    """Removes user from session and returns to homepage"""

    # Remove user ID from session
    session.pop('user', None)
    flash("You've been logged out.")

    # Sends user back to homepage with login form
    return redirect("/")


""" ** Routes related to cafes ** """

@app.route("/cafes", methods=["POST"])
def cafe_search():
    """Makes a Yelp API request with the user provided information.
    Displays an error message if the zipcode provided is invalid.
    Sends the user to the results page upon sucessful search.
    Displays the cafes returned from Yelp API request."""

    # Used to display navbar for logged in user
    login=True

    # Returns the cafes retrieved from the Yelp API request, using user provided info
    cafes = crud.get_cafes()

    # If provided zipcode isn't an integer or is negative
    if cafes == "error":
        flash("Please input a valid zipcode.")
        # Returns user back to search form to try again
        return redirect("/")

    # Sends user to results page; passes in cafes to display on page
    return render_template('results.html', cafes=cafes, login=login)
    

@app.route("/cafes/<cafe_id>")
def show_specific_cafe(cafe_id):
    """Retrieves all the information about the specific cafe.
    Saves the current cafe information in session.
    Sends the user to the details page.
    Displays the cafe information returned from Yelp API request."""

    # Used to display navbar for logged in user
    login=True

    # Returns information about the cafe from the Yelp API request, using the cafe ID
    yelp_cafe = crud.get_cafe_by_id(cafe_id)

    # Returns a dictionary of the hours of operation for the cafe
    hours = crud.get_cafe_hours(yelp_cafe)

    # Returns reviews of the cafe from the Yelp API request, using the cafe ID
    yelp_reviews= crud.get_yelp_reviews(cafe_id)

    # Returns the reformatted dates for the cafe reviews
    yelp_review_dates=crud.get_yelp_review_dates(yelp_reviews)

    # Saving all the cafe information in session
    session["cafe_id"] = cafe_id
    session["cafe_name"] = yelp_cafe["name"]
    session["image_url"] = yelp_cafe["image_url"]
    session["cafe_street"] = yelp_cafe["location"]["address1"]
    session["cafe_city"] = yelp_cafe["location"]["city"]
    session["cafe_state"] = yelp_cafe["location"]["state"]
    session["cafe_zip"] = yelp_cafe["location"]["zip_code"]

    # Returns the cafe ID for the cafe from the Google Places API request using the cafe name in session
    google_cafe_id = crud.get_google_cafe_id()

    # Returns the information about the cafe from the Google Places API request, using the cafe ID
    google_cafe = crud.get_google_cafe(google_cafe_id)

    # Returns just the reviews of the cafe from the previous Google Places API request response
    google_reviews = crud.get_google_reviews(google_cafe)

    # Checking the DB to see if the user has reviewed the cafe being displayed; Sets variable to true or false accordingly
    if Reviews.query.filter(Reviews.user_id==session["user"], Reviews.cafe_id==session["cafe_id"]).first():
        user_review = True
    else:
        user_review = False
    
    # Sends user to details page; passes in cafe information, reviews, and user information to display on page
    return render_template("details.html", yelp_cafe=yelp_cafe, yelp_reviews=yelp_reviews, yelp_review_dates=yelp_review_dates, hours=hours, google_cafe=google_cafe, google_reviews=google_reviews, user_review=user_review, login=login)


""" ** Routes related to user ** """

@app.route("/user/<user_id>")
def show_user_profile(user_id):
    """Retrieves the user and associated information.
    Sends the user to the profile page.
    Displays the user information."""

    # Used to display navbar for logged in user
    login=True

    # Grabs user using passed in user ID
    user = crud.get_user_by_id(user_id)

    # Grabs all the cafes the user has favorited
    favorite_cafes = crud.get_user_favorites(user_id)

    # Grabs all the cafes the user has reviewed
    user_reviews = crud.get_user_reviews()

    # Grabs the user's profile picture
    profile_pic = crud.get_profile_pic(user)

    # Sends user to profile page; passes in user info, profile pic, favorited cafes, reviewed cafes to display on page
    return render_template("profile.html", user=user, favorite_cafes=favorite_cafes, user_reviews=user_reviews, profile_pic=profile_pic, login=login)

@app.route("/upload-profile-pic", methods=["POST"])
def upload_profile_pic():
    """Grabs the user's uploaded image and uploads it to Cloudinary API.
    Saves Cloudinary profile picture URL to User table in DB.
    Sends user back to profile picture where new profile picture is displayed."""

    # Grabbing profile picture from user input
    user_image = request.files['profile-img']

    # Uploading profile picture using Cloudinary API
    result = cloudinary.uploader.upload(user_image, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUDINARY_NAME)

    # Grabbing image URL from Cloudinary API and saving to variable
    img_url = result['secure_url']

    #Grabs user using user ID in session
    user = crud.get_user_by_id(session['user'])

    # Adds profile pic to user's row in User DB
    user.user_image = img_url
    db.session.commit()

    # Sends user to same page where new profile pic is displayed
    return redirect(request.referrer)

@app.route("/get-profile-pic", methods=["POST"])
def get_profile_pic():
    """Checks to see if the user has a profile picture URL in the DB
    Returns the profile picture URL or a string if it does not exist"""

    # Grab user using the user ID in session
    user = crud.get_user_by_id(session['user'])

    # Grabs the profile picture URL from user's DB entry
    img_url = user.user_image

    # If the profile picture exists
    if img_url:
        return img_url
    # If the profile picture doesn't exist
    else:
        return "False"
    

""" ** Routes related to Google maps ** """
    # /results-coordinates and /results-markers used for Google map on results.html
    # /cafe-coordinates and /cafe-marker used for Google map on details.html

@app.route("/results-coordinates")
def retrieve_results_coordinates():
    """Returns the coordinates of the cafes retrieved from the Yelp API request.
    Used to display markers on Google map on results page."""

    # Uses the zipcode and radius in session to grab the cafes
    cafes = crud.get_cafes_with_session()

    # Creates a dictionary of the cafes' coordinates using API response
    coordinates = crud.get_cafe_coordinates(cafes)

    # Returns the cafes' coordinates to results-map.js to display markers on results map
    return coordinates

@app.route("/results-markers")
def retrieve_results_marker_info():
    """Returns the cafe information retrieved from the Yelp API request.
    Used to display info windows on Google map on results page."""

    # Uses the zipcode and radius in session to grab the cafes
    cafes = crud.get_cafes_with_session()

    # Creates a dictionary of the cafes' information using API response
    marker_info = crud.get_marker_info(cafes)

    # Returns the cafes' information to results-map.js to display info windows on results map
    return marker_info

@app.route("/cafe-coordinates")
def retrieve_cafe_coordinates():
    """Returns the coordinates of the cafe retrieved from the Yelp API request.
    Used to display marker on Google map on details page."""

    # Uses the cafe ID to grab the cafe info
    cafe = crud.get_cafe_by_id(session["cafe_id"])

    # Creates a dictionary of the latitude and longitude of the cafe from the cafe info
    coordinate = {'latitude' : cafe['coordinates']['latitude'], 'longitude': cafe['coordinates']['longitude']}

    # Returns the cafe's coordinates to cafe-map.js to display marker on cafe map
    return coordinate

@app.route("/cafe-marker")
def retrieve_cafe_marker_info():
    """Returns the cafe information retrieved from the Yelp API request.
    Used to display info window on Google map on details page."""

    # Uses the cafe ID to grab the cafe info
    cafe = crud.get_cafe_by_id(session["cafe_id"])

    # Creates a dictionary of the cafe's information using API response
    cafe_info = {'0': [cafe["name"], cafe["id"], cafe["location"]["address1"], cafe["location"]["city"], cafe["location"]["state"], cafe["location"]["zip_code"]]}

    # Returns the cafe's information to cafe-map.js to display info window on cafe map
    return cafe_info

""" ** Routes related to user actions ** """

# Favoriting routes

@app.route("/favorite")
def favorite():
    """Add cafe into Favorites table of DB"""

    # Setting date to time of favorites button click
    date = datetime.now()

    # Creating a variable for DB addition where table is Favorites and information is in session
    favorite = Favorites(user_id=session["user"], cafe_id=session["cafe_id"], date=date, cafe_name=session["cafe_name"], image_url=session["image_url"], 
    cafe_street=session["cafe_street"], cafe_city=session["cafe_city"], cafe_state=session["cafe_state"], cafe_zip=session["cafe_zip"])

    # Adding entry into DB
    db.session.add(favorite)
    db.session.commit()

    # Returning nothing
    return ''

@app.route("/unfavorite")
def unfavorite():
    """Remove cafe from Favorites table of DB"""
    
    # Finding DB entry in Favorites table where cafe ID and user ID are the same as those in session
    unfavorite = Favorites.query.filter((Favorites.cafe_id==session["cafe_id"]) & (Favorites.user_id==session["user"])).one()

    # Remove entry from DB
    db.session.delete(unfavorite)
    db.session.commit()

    # Returning nothing
    return ''

@app.route("/favorites-check")
def check_database():
    """Check to see if cafe is already in Favorites table of DB"""

    # Querying DB for a row in Favorites table where cafe ID and user ID are the same as those in session
    check = Favorites.query.filter((Favorites.cafe_id==session["cafe_id"]) & (Favorites.user_id==session["user"])).first()

    # If cafe is in Favorites table of DB for the logged in user
    if check is not None:
        return "True"
    # If cafe is not in Favorites table of DB for the logged in user
    else:
        return "False"

# Reviewing routes

@app.route("/user-reviews", methods=['POST'])
def retrieve_user_reviews():
    """Check DB for a review of the cafe by the user in the Reviews table
    Return the review or a string if it does not exist"""

    # Checking the Reviews table of the DB for an entry where cafe ID and user ID are the same as those in session
    # If review does exist
    if Reviews.query.filter(Reviews.user_id==session["user"], Reviews.cafe_id==session["cafe_id"]).first():

        # Create a variable to store the found review
        review = Reviews.query.filter(Reviews.user_id==session["user"], Reviews.cafe_id==session["cafe_id"]).first()

        # Return a dictionary with the formatted review date, rating, and review in JSON
        return jsonify({'date': review.date.strftime('%-m/%-d/%y %-I:%M %p'), 'rating': review.rating, 'review': review.review})
    
    # If review does not exist
    else:
        return "False"

@app.route("/reviewing", methods=['POST'])
def review():
    """Uses user's input to create an entry in Reviews table of DB.
    Returns a dictionary of review details."""

    # Grabbing user input
    rating = request.form.get("rating")
    text = request.form.get("review")

    # Setting date to time of form submission
    date = datetime.now()

    # Create a variable to store Reviews table database entry
    review = Reviews(user_id=session["user"], cafe_id=session["cafe_id"], date=date, rating=rating, review=text)

    # Adding entry into DB
    db.session.add(review)
    db.session.commit()

    # Return a dictionary with the formatted review date, rating, and review in JSON
    return jsonify({'date': review.date.strftime('%-m/%-d/%y %-I:%M %p'), 'rating': rating, 'review': text})

@app.route("/updating", methods=['POST'])
def review_edit():
    """Searchs DB for existing Reviews table entry for current user with current cafe.
    Updates DB entry with user's new input.
    Returns a dictionary of review details"""

    # Grabbing user input
    updated_rating = request.form.get("updatedrating")
    updated_text = request.form.get("updatedreview")

    # Setting date to time of form submission
    updated_date = datetime.now()

    # Querying DB for entry in Reviews table where user ID and cafe ID are those in session
    review = Reviews.query.filter(Reviews.user_id==session["user"], Reviews.cafe_id==session["cafe_id"]).first()

    #Updating date,rating, and review with new input
    review.date = updated_date
    review.rating = updated_rating
    review.review = updated_text

    # Updating DB
    db.session.commit()

    # Returning a dictionary eith the formatted review date, rating, and review in JSON
    return jsonify({'date': review.date.strftime('%-m/%-d/%y %-I:%M %p'), 'rating': updated_rating, 'review': updated_text})



if __name__ == '__main__':
    connect_to_db(app, "cafes")
    app.run(host='0.0.0.0', debug=True)
