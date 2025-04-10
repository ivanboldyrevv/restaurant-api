from unittest import mock

import pytest
from fastapi.testclient import TestClient

from app.services.table_service import TableService
from app.exceptions import NotFoundException
from app.main import app


@pytest.fixture()
def client():
    yield TestClient(app)


@pytest.fixture()
def mock_service():
    yield mock.Mock(spec=TableService)


def test_get_tables(client, mock_service):
    valid = [
        {"id": 0, "name": "test_table", "seats": 1, "location": "window"}
    ]
    mock_service.get_all.return_value = valid

    with app.container.table_service.override(mock_service):
        response = client.get("/tables/")

    assert response.status_code == 200
    assert response.json() == valid


def test_add_table(client, mock_service):
    valid = {"name": "test_table", "seats": 1, "location": "window"}

    response_model = valid
    response_model["id"] = 1

    mock_service.add_table.return_value = response_model

    with app.container.table_service.override(mock_service):
        response = client.post("/tables/", json=valid)

    assert response.status_code == 200
    assert response.json() == response_model


def test_delete_table(client, mock_service):
    valid = {"id": 1, "name": "test_table", "seats": 1, "location": "window"}

    mock_service.delete_by_id.return_value = valid

    with app.container.table_service.override(mock_service):
        response = client.delete("/tables/1")

    assert response.status_code == 204


def test_delete_with_exception(client, mock_service):
    mock_service.delete_by_id.side_effect = NotFoundException(1)

    with app.container.table_service.override(mock_service):
        response = client.delete("/tables/1")

    assert response.status_code == 404
