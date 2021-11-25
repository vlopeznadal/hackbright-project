from unittest import TestCase

from flask.helpers import flash
from server import app
from model import connect_to_db, db, example_data, User
from flask import session

class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_home(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"Login", result.data)

    def test_logout(self):
        result = self.client.get('/logout', follow_redirects = True)
        self.assertIn(b"Login", result.data)

class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 1

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"email": "leonard@test.com", "password": "leo123"},
                                  follow_redirects=True)
        self.assertIn(b"Zip Code", result.data)

    def test_cafes(self):
        """Test results page."""

        result = self.client.post("/cafes",
                                  data={"zipcode": 55404},
                                  follow_redirects=True)
        self.assertIn(b"Alma", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()