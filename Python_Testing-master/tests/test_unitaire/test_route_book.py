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


def test_book_competition_past(client):
    """Test pour vérifier si un club peut booker une compétition passée"""
    response = client.get("/book/Spring Festival/Iron Temple")

    assert response.status_code == 200
    assert b"Erreur : Vous ne pouvez pas vous inscrire a une competition deja passee" in response.data
    #Test Ok


def test_book_competition_futur(client):
    """Test pour vérifier si un club peut booker une compétition future"""
    response = client.get("/book/JO/Iron Temple")

    assert response.status_code == 200
    # Test OK

