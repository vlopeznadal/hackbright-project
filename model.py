"""Models for cafe information app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    user_image = db.Column(db.String(100))

    favorites = db.relationship("Favorites", back_populates="user")
    reviews = db.relationship("Reviews", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

class Favorites(db.Model):
    """A favorite cafe."""

    __tablename__ = "favorites"

    query_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    date = db.Column(db.DateTime, nullable=False)
    cafe_id = db.Column(db.String(50), nullable=False)
    cafe_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(100))
    cafe_street = db.Column(db.String(50), nullable=False)
    cafe_city = db.Column(db.String(50), nullable=False)
    cafe_state = db.Column(db.String(50), nullable=False)
    cafe_zip = db.Column(db.String(50), nullable=False)

    user = db.relationship("User", back_populates="favorites")

    def __repr__(self):
        return f"<Favorites query_id={self.query_id} user_id={self.user_id} cafe_id={self.cafe_id}>"

class Reviews(db.Model):
    """A cafe review."""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    cafe_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(500))

    user = db.relationship("User", back_populates="reviews")

    def __repr__(self):
        return f"<Reviews review_id={self.review_id} user_id={self.user_id} date={self.date}>"

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()

    # Add sample users
    leonard = User(email='leonard@test.com', password="leo123")
    liz = User(email='liz@test.com', password="liz123")
    maggie = User(email='maggie@test.com', password="mag123")
    nadine = User(email='nadine@test.com', password="nad123")

    db.session.add_all([leonard, liz, maggie, nadine])
    db.session.commit()

def connect_to_db(app, db_name):
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app, "cafes")