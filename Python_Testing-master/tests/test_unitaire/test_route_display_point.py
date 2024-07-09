import sys
import os
import pytest

# Determine the absolute path of the parent directory
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '../../../Python_Testing-master'))

# Add the parent directory to PYTHONPATH
sys.path.insert(0, parent_dir)

# Import functions from server.py
from server import loadClubs, app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'something_special'
    app.clubs = loadClubs()

    client = app.test_client()
    return client

def test_purchasePlaces(client):
    """Test pour vérifier si un club peut booker des places dans une compétition existante"""
    data = {
        "competition": "Fall Classic",
        "club": "She Lifts",
        "places": "3",
    }
    response = client.post("/purchasePlaces", data=data)

    # Vérification du code de statut HTTP
    assert response.status_code == 200

    # TEST OK


def test_purchasePlaces_not_enough_points(client):
    """Test pour vérifier si un club peut booker plus de places qu'il a de points"""
    data = {
        "competition": "Spring Festival",
        "club": "Iron Temple",  # Use a valid club name
        "places": "12",
    }
    response = client.post("/purchasePlaces", data=data)
    assert response.status_code == 403  # 403 : Accès refusé

    # Test OK


def test_purchasePlaces_negative_places(client):
    """Test pour vérifier si un club peut booker un nombre de place négatif"""
    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "-3",
    }
    response = client.post("/purchasePlaces", data=data)

    # Vérification du code de statut HTTP
    assert response.status_code == 403  # 403 : Accès refusé

    # Test OK


def test_purchasePlaces_max_places_exceeded(client):
    """Test pour vérifier si un club peut booker un nombre de place > nombre de points disponible"""
    data = {
        "competition": "Spring Festival",
        "club": "Iron Temple",
        "places": "5",
    }
    response = client.post("/purchasePlaces", data=data)

    # Vérification du code de statut HTTP
    assert response.status_code == 403
    # Test Ok


def test_purchasePlaces_too_many_places(client):
    """Test pour vérifier si un club peut booker un nombre de place >12"""
    data_too_many_places = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "30",
    }
    response_too_many_places = client.post(
        "/purchasePlaces", data=data_too_many_places
    )
    assert response_too_many_places.status_code == 403

    # Test OK

def test_purchasePlaces_no_places_specified(client):
    """Test pour vérifier si un club peut booker un nombre de place =0"""
    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "0",
    }
    response_no_places = client.post("/purchasePlaces", data=data)
    assert response_no_places.status_code == 403

def test_display_points(client):
    """Test to check if the points display page is shown correctly"""
    response = client.get("/pointsBoard")
    assert response.status_code == 200
