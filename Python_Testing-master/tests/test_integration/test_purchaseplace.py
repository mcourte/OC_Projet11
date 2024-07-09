import pytest
from flask_testing import TestCase
import json
import os
import sys

# Determining the absolute path of the parent directory
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '../../../Python_Testing-master'))

# Adding the parent directory to the PYTHONPATH
sys.path.insert(0, parent_dir)

# Importing functions from server.py
from server import loadClubs, loadCompetitions, app

def reset_data():
    initial_competitions = loadCompetitions()
    initial_clubs = loadClubs()

    with open("competitions.json", "w") as f:
        json.dump({"competitions": initial_competitions}, f, indent=4)
    with open("clubs.json", "w") as f:
        json.dump({"clubs": initial_clubs}, f, indent=4)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'something_special'
    client = app.test_client()
    reset_data()  # Ensure fresh data for each test
    return client

@pytest.mark.integtest
class FunctionalTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.secret_key = 'something_special'
        return app

    def setUp(self):
        reset_data()
        with open("competitions.json", "r") as f:
            self.competitions = json.load(f)["competitions"]
        with open("clubs.json", "r") as f:
            self.clubs = json.load(f)["clubs"]
        app.competitions = self.competitions
        app.clubs = self.clubs

    def test_purchase_places(self):
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "1",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 200

    def test_point_decrement(self):
        club = next(c for c in self.clubs if c['name'] == "Simply Lift")
        initial_point = int(club["points"])
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "1",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 200

        with open("clubs.json", "r") as f:
            updated_clubs = json.load(f)["clubs"]
        updated_club = next(c for c in updated_clubs if c['name'] == "Simply Lift")
        updated_point = int(updated_club["points"])
        assert updated_point == initial_point - 1

    def test_purchasePlaces_not_enough_points(self):
        data = {
            "competition": "Spring Festival",
            "club": "She Lifts",
            "places": "12",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 403

    def test_purchasePlaces_negative_places(self):
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "-3",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 403

    def test_purchasePlaces_max_places_exceeded(self):
        data = {
            "competition": "Spring Festival",
            "club": "Iron Temple",
            "places": "15",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 403

    def test_purchasePlaces_too_many_places(self):
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "30",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 403

    def test_purchasePlaces_no_places_specified(self):
        data = {
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "0",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 403
