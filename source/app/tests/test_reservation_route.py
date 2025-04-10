from datetime import datetime
from unittest import mock
import types

import pytest
from fastapi.testclient import TestClient

from app.services.reservation_service import ReservationService
from app.exceptions import (CreateReservationException,
                            ExistingReservationException,
                            NotFoundException)
from app.main import app


@pytest.fixture()
def client():
    yield TestClient(app)


@pytest.fixture
def service_mock():
    class MockedService:
        def __init__(self):
            self._calls = []

        def add_reservation(self, *args, **kwargs):
            self._calls.append((args, kwargs))
            if len(self._calls) > 1:
                raise ExistingReservationException(
                    "This reservation conflicts with another one.",
                    datetime.now()
                )
            if kwargs.get("table_id") == 2:
                raise CreateReservationException("No table")
            return {"id": 1, **kwargs}

    service_mock = mock.Mock(spec=ReservationService)
    service_mock._calls = []
    service_mock.add_reservation = types.MethodType(
        MockedService.add_reservation,
        service_mock
    )

    yield service_mock


def test_get_reservations(client, service_mock):
    today = datetime.now()

    service_mock.get_all.return_value = [{
        "customer_name": "test_name",
        "table_id": 0,
        "reservation_time": today.isoformat(),
        "duration_minutes": 60,
        "id": 0
    }]

    with app.container.reservation_service.override(service_mock):
        response = client.get("/reservations/")
        content = response.json()

    expected = [{
        "customer_name": "test_name",
        "table_id": 0,
        "reservation_time": today.isoformat(),
        "duration_minutes": 60,
        "id": 0
    }]

    assert response.status_code == 200
    assert content == expected


def test_add_reservation_valid(client, service_mock):
    test_data = {
        "customer_name": "test",
        "table_id": 1,
        "reservation_time": datetime.now().isoformat(),
        "duration_minutes": 30
    }

    with app.container.reservation_service.override(service_mock):
        response = client.post("/reservations/", json=test_data)

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_raise_reservation_exception(client, service_mock):
    test_data = {
        "customer_name": "test",
        "table_id": 1,
        "reservation_time": datetime.now().isoformat(),
        "duration_minutes": 30
    }

    with app.container.reservation_service.override(service_mock):
        response = client.post("/reservations/", json=test_data)
        assert response.status_code == 200

        response = client.post("/reservations/", json=test_data)
        assert response.status_code == 409


def test_raise_table_exception(client, service_mock):
    test_data = {
        "customer_name": "test",
        "table_id": 2,
        "reservation_time": datetime.now().isoformat(),
        "duration_minutes": 30
    }

    with app.container.reservation_service.override(service_mock):
        response = client.post("/reservations/", json=test_data)
        assert response.status_code == 409


def test_delete_by_id(client, service_mock):
    service_mock.delete_by_id.return_value = True

    with app.container.reservation_service.override(service_mock):
        response = client.delete("/reservations/0")

    assert response.status_code == 204


def test_raise_delete(client, service_mock):
    service_mock.delete_by_id.side_effect = NotFoundException(1)

    with app.container.reservation_service.override(service_mock):
        response = client.delete("/reservations/1")

    assert response.status_code == 404


def test_wrong_minutes(client):
    test_data = {
        "customer_name": "test",
        "table_id": 2,
        "reservation_time": datetime.now().isoformat(),
        "duration_minutes": -30
    }

    response = client.post("/reservations/", json=test_data)

    assert response.status_code == 422
