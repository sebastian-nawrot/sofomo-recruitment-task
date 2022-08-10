from fastapi.testclient import TestClient
from pymongo.errors import PyMongoError
from pymongo.results import DeleteResult
from starlette import status
from unittest.mock import patch
import json
import requests

from app.app import app, collection
from app.authentication import generate_access_token, verify_access_token
from tests.fixtures.geolocation_fixtures import *
from tests.fixtures.ip_stack_api_fixtures import *


client = TestClient(app)


class TestAuthentication:
  def test_generate_access_token(self):
    response = client.get("/access_token")
    assert response.status_code == status.HTTP_200_OK

    # Shouldn't raise exception
    verify_access_token(response.json()["access-token"])


# Set authentication token for all requests
access_token = generate_access_token()
client.headers = { "access-token": access_token }


class TestGetGeolocation:
  URL = "/geolocation/172.152.31.241"

  @patch.object(collection, "find_one")
  def test_200_response(self, mock_find_one, geolocation_data_fixture):
    mock_find_one.return_value = geolocation_data_fixture
    response = client.get(self.URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == geolocation_data_fixture

  @patch.object(collection, "find_one")
  def test_404_response(self, mock_find_one):
    mock_find_one.return_value = None
    response = client.get(self.URL)
    assert response.status_code == status.HTTP_404_NOT_FOUND

  @patch.object(collection, "find_one")
  def test_500_response(self, mock_find_one):
    mock_find_one.side_effect = PyMongoError()
    response = client.get(self.URL)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == { "detail": "The server encountered an internal error" }



class TestDeleteGeolocation:
  URL = "/geolocation/172.152.31.241"

  @patch.object(collection, "delete_one")
  def test_204_response(self, mock_delete_one):
    mock_delete_one.return_value = DeleteResult({ "n": 1, "ok": 1.0}, True)
    response = client.delete(self.URL)
    assert response.status_code == status.HTTP_204_NO_CONTENT

  @patch.object(collection, "delete_one")
  def test_404_response(self, mock_delete_one):
    mock_delete_one.return_value = DeleteResult({ "n": 0, "ok": 1.0}, True)
    response = client.delete(self.URL)
    assert response.status_code == status.HTTP_404_NOT_FOUND

  @patch.object(collection, "delete_one")
  def test_500_response(self, mock_delete_one):
    mock_delete_one.side_effect = PyMongoError()
    response = client.delete(self.URL)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == { "detail": "The server encountered an internal error" }



class TestPostGeolocation:
  URL = "/geolocation"

  @patch.object(collection, "update_one")
  @patch.object(requests, "get")
  def test_201_response(self, mock_get, mock_update_one, ip_stack_api_correct_response_fixture):
    response = requests.Response()
    response.status_code = status.HTTP_200_OK
    response._content = json.dumps(ip_stack_api_correct_response_fixture).encode()
    mock_get.return_value = response

    # Just to prevent request
    mock_update_one.return_value = None

    response = client.post(self.URL, json={"address": "172.152.31.241"})
    assert response.status_code == status.HTTP_201_CREATED

  @patch.object(collection, "update_one")
  @patch.object(requests, "get")
  def test_500_response(self, mock_get, mock_update_one, ip_stack_api_error_response_fixture):
    response = requests.Response()
    response.status_code = status.HTTP_200_OK
    response._content = json.dumps(ip_stack_api_error_response_fixture).encode()
    mock_get.return_value = response

    # Just to prevent request
    mock_update_one.return_value = None

    response = client.post(self.URL, json={"address": "172.152.31.241"})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
