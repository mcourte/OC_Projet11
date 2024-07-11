import sys
import os
import pytest


# Déterminez le chemin absolu du répertoire parent
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '../../../Python_Testing-master'))

# Ajoutez le répertoire parent au PYTHONPATH
sys.path.insert(0, parent_dir)

# Vérifiez le contenu de sys.path (pour le débogage)
print("sys.path:", sys.path)

# Importez les fonctions depuis server.py
from server import loadClubs, loadCompetitions, app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'something_special'
    app.clubs = loadClubs()
    app.competitions = loadCompetitions()

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
    """Test pour vérifier si un club peut booker plus de places qu'il a de point"""
    data = {
        "competition": "Spring Festival",
        "club": "Iron Temple",
        "places": "12",
    }
    response = client.post("/purchasePlaces", data=data)

    # Vérification du code de statut HTTP
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
        "club": "Simply Lift",
        "places": "15",
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

def test_purchasePlace_more_than_remaining(client):
    """Test pour vérifier si un club peut booker un nombre de place > nombre de place restant"""
    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "0",
    }
    response_no_enough_places = client.post("/purchasePlaces", data=data)
    assert response_no_enough_places.status_code == 403
 
def test_purchasePlace_more_than_12_in_different_book(client):
    """Test pour vérifier si un club peut booker un nombre de place > nombre de place restant"""
    data1 = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "9",
    }
    data2 = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "4",
    }
    response_places = client.post("/purchasePlaces", data=data1)
    assert response_places.status_code == 200
    
    response_too_much_places = client.post("/purchasePlaces", data=data2)
    assert response_too_much_places.status_code == 403