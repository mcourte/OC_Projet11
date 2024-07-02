import pytest
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

    assert response.status_code == 400
    # LE RETOUR ACTUEL EST " STATUS_CODE == 200"


def test_book_competition_futur(client):
    """Test pour vérifier si un club peut booker une compétition future"""
    response = client.get("/book/Go JO/Iron Temple")

    assert response.status_code == 200
    # Test OK
