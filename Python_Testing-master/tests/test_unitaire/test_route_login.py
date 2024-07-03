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

def test_logout(client):
    """Test pour vérifier que si l'utilisateur se déconnecte il retourne bien sur la page de connexion"""
    response = client.get('/logout')
    # Vérification que la réponse est bien une redirection
    assert response.status_code == 302

    # Vérification que la redirection va bien sur la page demandée
    assert response.headers['Location'] == 'http://localhost/'
