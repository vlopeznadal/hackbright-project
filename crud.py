"""CRUD operations."""

from model import db, User, Favorites, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_user(email):
    """Get a user if email exists, otherwise return none"""
    
    return User.query.filter(User.email == email).first()