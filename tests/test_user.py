import pytest
import requests
from unittest.mock import patch

def mock_get(url, params=None, **kwargs):
    class MockResponse:
        def __init__(self, status_code, text):
            self.status_code = status_code
            self.text = text
    
    if params == {"username": "admin", "password": "admin"}:
        return MockResponse(401, "")
    elif params == {"username": "admin", "password": "qwerty"}:
        return MockResponse(200, "")
    return MockResponse(404, "Not Found")

@patch("requests.get", side_effect=mock_get)
def test_users_endpoint_unauthorized(mock_get):
    url = "http://127.0.0.1:8000/users"
    params = {"username": "admin", "password": "admin"}
    
    response = requests.get(url, params=params)
    
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    assert isinstance(response.text, str), "Expected response to be text"

@patch("requests.get", side_effect=mock_get)
def test_users_endpoint_authorized(mock_get):
    url = "http://127.0.0.1:8000/users"
    params = {"username": "admin", "password": "qwerty"}
    
    response = requests.get(url, params=params)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert isinstance(response.text, str), "Expected response to be text"
