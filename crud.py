"""CRUD operations."""
from flask import (request)
from model import db, User, Favorites, connect_to_db
import requests, os

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_user(email):
    """Get a user if email exists, otherwise return none"""
    
    return User.query.filter(User.email == email).first()

def get_user_by_id(user_id):

    return User.query.filter(User.user_id == user_id).first()

def get_user_favorites(user_id):

    return Favorites.query.filter(Favorites.user_id == user_id).all()

def get_cafes():
    zipcode = request.form.get("zipcode")
    radius = request.form.get("radius")

    try:
        int(zipcode)
    except ValueError:
        return "error"

    if int(zipcode) < 0:
        return "error"

    location = {'categories': 'cafes', 'location': zipcode, 'radius': radius, 'limit': 5}
    headers= {'Authorization': 'Bearer ' + os.environ['YELP_KEY']}

    res = requests.get('https://api.yelp.com/v3/businesses/search',
                   params=location, headers=headers)

    cafe_search = res.json()

    cafes = cafe_search['businesses']
    
    return cafes

def get_cafe_by_id(cafe_id):
    headers= {'Authorization': 'Bearer ' + os.environ['YELP_KEY']}
    res = requests.get(f'https://api.yelp.com/v3/businesses/{cafe_id}', headers=headers)
    cafe_info = res.json()

    return cafe_info

def get_cafe_reviews(cafe_id):
    headers= {'Authorization': 'Bearer ' + os.environ['YELP_KEY']}
    res = requests.get(f'https://api.yelp.com/v3/businesses/{cafe_id}/reviews', headers=headers)
    cafe_reviews = res.json()

    reviews = cafe_reviews['reviews']

    return reviews
