"""CRUD operations."""
from flask import (request, session)
from model import db, User, Favorites, Reviews
import datetime
import requests, os

YELP_KEY = os.environ['YELP_KEY']


""" ** User login and registration functions ** """

def get_user(email):
    """Get a user if user with email exists in DB, otherwise return None"""
    
    # Return user if found in DB with provided email
    return User.query.filter(User.email == email).first()

def create_user(email, password):
    """Create a new user in DB and return the new user."""

    # Create a new row in User table of DB with the provided email and password
    user = User(email=email, password=password)

    # Add user into User table of DB
    db.session.add(user)
    db.session.commit()

    # Return the created user
    return user


""" ** User-related functions """

def get_user_by_id(user_id):
    """Get a user if user with ID exists in DB, otherwise return None"""

    # Return user if found in DB with provided user ID
    return User.query.filter(User.user_id == user_id).first()

def get_profile_pic(user):
    """Grabs user's profile picture from DB and returns it"""

    # Getting the provided user's profile picture from DB
    profile_pic = user.user_image

    # Returns profile picture URL
    return profile_pic

def get_user_favorites(user_id):
    """Gets all the user's favorited cafes from the DB"""

    # Querying Favorites table of DB for all entries with provided user ID
    return Favorites.query.filter(Favorites.user_id == user_id).all()

def get_user_reviews():
    """Gets all the user's reviewed cafes from the DB.
    Grabs the names and IDs of the reviewed cafes.
    Returns a tuple of lists with all this information."""

    # Checking to see if user has any reviewed cafes
    # If user has reviewed at least one cafe
    if Reviews.query.filter(Reviews.user_id==session["user"]).first():
        # Setting a variable to all reviews done by the user; limits to 5
        reviews = Reviews.query.filter(Reviews.user_id==session["user"]).limit(5).all()
    # If user has not reviewed any cafes
    else:
        return ""
    
    # Create empty list
    cafes = []

    # For each review in query results
    for review in reviews:

        # Get the cafe information for the cafe using its ID
        cafe = get_cafe_by_id(review.cafe_id)

        # Add the name of the cafe to the list
        cafes.append([review.cafe_id, cafe['name']])

    # Returns a tuple of lists of the reviews and the cafe IDs and names
    return reviews, cafes


""" ** Cafe-related functions ** """

def get_cafes():
    """Using user provided zipcode and radius to do a Yelp API request.
    Checks for valid zipcode input and returns error if not valid.
    Returns cafe results from API call."""

    # Grabbing entered in zipcode and selected radius
    zipcode = request.form.get("zipcode")
    radius = request.form.get("radius")

    # Saving zipcode and radius in session
    session["zipcode"] = zipcode
    session["radius"] = radius

    # Checking for valid zipcode
    try:
        # Checking if zipcode is an integer
        int(zipcode)
    except ValueError:
        return "error"

    # Checking if zipcode is negative
    if int(zipcode) < 0:
        return "error"

    # Parameters for Yelp API request, including provided zipcode and radius
    location = {'categories': 'cafes', 'location': session["zipcode"], 'radius': session["radius"], 'limit': 6}
    headers= {'Authorization': 'Bearer ' + YELP_KEY}

    # Yelp API request searching for cafes; Returning a limit of 6
    res = requests.get('https://api.yelp.com/v3/businesses/search',
                   params=location, headers=headers)

    # Turning response into JSON
    cafe_search = res.json()

    # Limiting results to just the businesses found
    cafes = cafe_search['businesses']
    
    # Returning found businesses to /cafes route in server.py
    return cafes

def get_google_cafe_id():
    """Using the cafe name in session to do a Google Places API request for the cafe's ID.
    Returns the cafe ID from API call."""

    # Parameters for Google Places API request, including the cafe name from session
    location = {'fields': 'place_id', 'input': session["cafe_name"], 'inputtype': 'textquery', 'key': 'AIzaSyD2MwTqduMNK_g-86AK2g72L5NOsWAMBk0'} 

    # Google Places API request searching for cafe 
    res = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json', 
                    params=location)

    # Turning response into JSON
    cafe = res.json()

    # Limiting result to just the cafe ID
    cafe_id = cafe["candidates"][0]["place_id"]
    
    # Returning the ID of the particular cafe
    return cafe_id

def get_cafes_with_session():
    """Using zipcode and radius in session to do a Yelp API request for a selection of cafes.
    Returns cafe results from API call."""

    # Parameters for Yelp API request, including zipcode and radius from session
    location = {'categories': 'cafes', 'location': session["zipcode"], 'radius': session["radius"], 'limit': 6}
    headers= {'Authorization': 'Bearer ' + YELP_KEY}

    # Yelp API request searching for cafes; Returning a limit of 6
    res = requests.get('https://api.yelp.com/v3/businesses/search',
                   params=location, headers=headers)

    # Turning response into JSON
    cafe_search = res.json()

    # Limiting results to just the businesses found
    cafes = cafe_search['businesses']
    
    # Returning found businesses to 2 map routes in server.py
    return cafes

def get_cafe_by_id(cafe_id):
    """Using cafe ID to do a Yelp API request for a particular cafe.
    Returns cafe results from API call."""

    # Parameters for Yelp API request; API key
    headers= {'Authorization': 'Bearer ' + YELP_KEY}

    # Yelp API request searching for cafe using cafe ID; Returning only 1
    res = requests.get(f'https://api.yelp.com/v3/businesses/{cafe_id}', headers=headers)

    # Turning response into JSON
    cafe_info = res.json()

    # Returning the information for the specific cafe
    return cafe_info


""" ** Cafe details functions ** """

def get_yelp_reviews(cafe_id):
    """Using cafe ID to do a Yelp API request for the reviews of a particular cafe.
    Returns the cafe reviews from API call."""

    # Parameters for Yelp API request; API key
    headers= {'Authorization': 'Bearer ' + YELP_KEY}

    # Yelp API request searching for reviews of cafe using cafe ID; Returning 3 reviews
    res = requests.get(f'https://api.yelp.com/v3/businesses/{cafe_id}/reviews', headers=headers)

    # Turning response into JSON
    cafe_reviews = res.json()

    # Grabbing only the reviews from response
    reviews = cafe_reviews['reviews']

    # Returning the review for the specific cafe
    return reviews

def get_yelp_review_dates(reviews):
    """Reformats the review dates returned by the Yelp API request.
    Inserts the reformatted dates into a list.
    Returns the list of reformatted review dates."""

    # Creates an empty list
    review_dates = []

    # For each review (limit of 3 by API)
    for i in range(3):

        # Grabbing the review date from Yelp API response
        date = reviews[i]['time_created']

        # Reformatting the review date and time
        formatted_date = datetime.datetime.strptime(date, '%Y-%m-%d  %H:%M:%S').strftime('%-m/%-d/%y %-I:%M %p')

        # Adding reformatted date to list
        review_dates.append(formatted_date)

    # Returning the list of reformatted review dates for the cafe
    return review_dates

def get_google_cafe(cafe_id):
    """Using the cafe ID to do a Google Places API request for the cafe information.
    Returns the cafe information from API call."""

    # Parameters for Google Places API request, including the cafe ID
    location = {'place_id': cafe_id, 'key': 'AIzaSyD2MwTqduMNK_g-86AK2g72L5NOsWAMBk0'} 

    # Google Places API request searching for cafe information for specific cafe
    res = requests.get('https://maps.googleapis.com/maps/api/place/details/json?fields=rating%2Creview%2Cwebsite', 
                    params=location)

    # Turning response into JSON
    cafe = res.json()

    # Limiting results to just the cafe information
    cafe_info = cafe["result"]
    
    # Returning the information of the specific cafe
    return cafe_info

def get_google_reviews(google_cafe):

    """Limits the Google Places API request response to just the reviews.
    Returns the reviews of the specific cafe."""
    
    # Returns the reviews of the specific cafe
    return google_cafe['reviews']

def get_cafe_hours(cafe):
    """Creates a dictionary of the hours of operation for the cafe.
    Includes a boolean of whether it is open or not now."""

    # Create an empty dictionary for hours
    cafe_hours = {}

    # For the length of the 'hours' list from Yelp API request response
    for i in range(len(cafe["hours"][0]["open"])):

        # Grabbing the opening time for the cafe from Yelp API request response of cafe info
        open = cafe["hours"][0]["open"][i]["start"]

        # Grabbing the closing time for the cafe from Yelp API request response of cafe info
        close = cafe["hours"][0]["open"][i]["end"]

        # Formatting the opening time
        formatted_open = datetime.datetime.strptime(open, '%H%M').strftime('%-I:%M %p')

        # Formatting the closing time
        formatted_close = datetime.datetime.strptime(close, '%H%M').strftime('%-I:%M %p')

        # Creating a variable of the weekday
        index = cafe["hours"][0]["open"][i]["day"]

        # Create an item in the dictionary where key is the weekday and
        # value is a list of the formatted open and close times
        cafe_hours[index] = [formatted_open, formatted_close]

    # Include whether the cafe is open or not as last item in dictionary
    cafe_hours[7] = cafe["hours"][0]["is_open_now"]

    # Returning the dictionary of hours for the specific cafe
    return cafe_hours


""" ** Map-related functions ** """   

def get_cafe_coordinates(cafes):
    """Creates a dictionary of the cafes' coordinates usiny Yelp API response.
    Returns coordinate dictionary to results-map.js
    Used to create markers to display on results map."""

    # Create an empty dictionary
    coordinates = {}

    # Initalize counter variable at 0
    counter = 0

    # For each cafe in the Yelp API response
    for cafe in cafes:

        # Create an item in the dictionary where key is a number starting at 0 and 
        # value is a dictionary of the cafe's longitude and latitude
        coordinates[counter]= cafe["coordinates"]

        # Increase couter by 1
        counter += 1
    
    # Return dictionary of coordinates to results-map.js
    return coordinates

def get_marker_info(cafes):
    """Creates a dictionary of the cafes' coordinates usiny Yelp API response.
    Returns coordinate dictionary to results-map.js
    Used to create markers to display on results map."""

    # Create an empty dictionary
    cafe_info = {}

    # Initalize counter variable at 0
    counter = 0

    # For each cafe in the Yelp API response
    for cafe in cafes:

        # Create an item in the dictionary where key is a number starting at 0 and
        # value is a list of the cafe's name, ID, and location (address, city, state, zip code)
        cafe_info[counter]= cafe["name"], cafe["id"], cafe["location"]["address1"], cafe["location"]["city"], cafe["location"]["state"], cafe["location"]["zip_code"]

        # Increase counter by 1
        counter += 1
    
    # Return dictionary of information to results-map.js
    return cafe_info

