"""Models for cafe information app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    favorites = db.relationship("Favorites", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

class Favorites(db.Model):
    """A favorite cafe."""

    __tablename__ = "favorites"

    query_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    cafe_id = db.Column(db.String(50), nullable=False)
    cafe_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(50))
    cafe_address = db.Column(db.String, nullable=False)

    user = db.relationship("User", back_populates="favorites")

    def __repr__(self):
        return f"<Favorites query_id={self.query_id} user_id={self.user_id} cafe_id={self.cafe_id}>"

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