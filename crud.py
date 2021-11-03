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

def get_cafes():
    zipcode = request.form.get("zipcode")
    radius = request.form.get("radius")

    location = {'categories': 'cafes', 'location': zipcode, 'radius': radius, 'limit': 5}
    headers= {'Authorization': 'Bearer ' + os.environ['YELP_KEY']}

    res = requests.get('https://api.yelp.com/v3/businesses/search',
                   params=location, headers=headers)

    cafe_search = res.json()

    cafes = cafe_search['businesses']

    # cafe_ids = []

    # for cafe in cafes:
    #     cafe_ids.append(cafe['id'])
    
    return cafes

# def get_cafe_info(cafe_ids):
#     all_cafes = []
#     headers= {'Authorization': 'Bearer ' + os.environ['YELP_KEY']}
#     for id in cafe_ids:
#         res2 = requests.get(f'https://api.yelp.com/v3/businesses/{id}', headers=headers)
#         cafe_info = res2.json()
#         all_cafes.append(cafe_info)
#     print(all_cafes)
#     return all_cafes
