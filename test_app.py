import pytest
from app import app

@pytest.fixture
def client():
    """Creates a test client for testing the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Checks the response code of the home page."""
    response = client.get('/')
    assert response.status_code == 200

def test_generate_endpoint(client):
    response = client.post('/generate', data={'isTest': True}, follow_redirects=True)
    assert response.status_code == 200

def test_invalid_generate_request(client):
    """Sends an invalid generate request and checks the response code."""
    response = client.post('/generate', data={}, follow_redirects=True)
    assert response.status_code == 400
