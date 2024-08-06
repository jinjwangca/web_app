import pytest
from applications.web.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the /health-check endpoint"""
    response = client.get('/health-check')
    assert response.status_code == 200
    assert response.json == {'message': 'I am healthy'}

def test_hello(client):
    """Test the /hello endpoint"""
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.json == {'message': 'Hello, World!'}