import sys
import os
import pytest
import json


# Déterminez le chemin absolu du répertoire parent
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '../../../Python_Testing-master'))

# Ajoutez le répertoire parent au PYTHONPATH
sys.path.insert(0, parent_dir)

# Vérifiez le contenu de sys.path (pour le débogage)
print("sys.path:", sys.path)

# Importez les fonctions depuis server.py
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
    app.clubs = loadClubs()
    app.competitions = loadCompetitions()

    client = app.test_client()
    return client


def test_index(client):
    """Test pour vérifier qu'on peut bien se connecter au serveur"""
    # Utilisez le client pour envoyer une requête GET à l'URL de l'index
    response = client.get('/')

    # Vérifiez que la réponse est réussie (code HTTP 200)
    assert response.status_code == 200
    # Test OK


def test_show_summary(client):
    """Test pour vérifier qu'on peut bien accéder à showSummary avec un club exitant & mail valide"""

    test_email = 'admin@irontemple.com'
    data = {'email': test_email}
    response = client.post('/showSummary', data=data)

    # Vérification du code de statut HTTP
    assert response.status_code == 200
    # Test OK


def test_no_email(client):
    """Test pour vérifier qu'on peut bien accéder à showSummary avec un mail vide"""

    response = client.post("/showSummary", data={"email": ""})

    # Vérification du code de statut HTTP
    assert response.status_code == 401
    # Test OK


def test_invalid_email(client):
    """Test pour vérifier qu'on peut bien accéder à showSummary avec un mail inexistant"""

    data = {"email": "invalid@example.com"}
    response = client.post("/showSummary", data=data)

    # Vérification du code de statut HTTP
    assert response.status_code == 401
    # Test OK


def test_book_competition_past(client):
    """Test pour vérifier si un club peut booker une compétition passée"""
    response = client.get("/book/Spring Festival/Iron Temple")

    assert response.status_code == 200
    assert b"Erreur" in response.data
    # Test Ok


def test_book_competition_futur(client):
    """Test pour vérifier si un club peut booker une compétition future"""
    response = client.get("/book/JO/Iron Temple")

    assert response.status_code == 200
    # Test OK


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
        "club": "Iron Temple",
        "places": "10",
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


def test_index_page_contains_points_board_link(client):
    """Test to check if the index page contains a link to the points board page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'Tableau des points' in response.data


def test_display_points(client):
    """Test to check if the points display page is shown correctly"""
    response = client.get("/pointsBoard")
    assert response.status_code == 200
    # Check the content to ensure points are displayed
    assert b'Points Board' in response.data
    assert b'Club' in response.data
    assert b'Points' in response.data


def test_logout(client):
    """Test pour vérifier que si l'utilisateur se déconnecte il retourne bien sur la page de connexion"""
    response = client.get('/logout')
    # Vérification que la réponse est bien une redirection
    assert response.status_code == 302

    # Vérification que la redirection va bien sur la page demandée
    assert response.headers['Location'] == '/'
    # Test Ok
