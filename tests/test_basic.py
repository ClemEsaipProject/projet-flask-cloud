import sys
import os
import pytest

# Ajouter le répertoire racine au sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Maintenant, pytest peut trouver le module app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_events_endpoint(client):
    response = client.get('/api/events')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    # Vérification conditionnelle des données
    if response.json:
        assert 'titre' in response.json[0]


def test_news_endpoint(client):
    response = client.get('/api/news')
    assert response.status_code == 200
    assert 'auteur' in response.json[0]
