from datetime import datetime, timedelta

from app.models import Reservation
from app.services.reservation_service import ReservationService

from unittest import mock
import pytest


@pytest.fixture()
def service():
    database_mock = mock.MagicMock()
    return ReservationService(database=database_mock)


def test_time_conflict_True(service):
    reservations = [
        Reservation(
            id=0,
            customer_name="customer_1",
            table_id=0,
            reservation_time=datetime.now(),
            duration_minutes=15
        )
    ]

    service.get_all = mock.MagicMock(return_value=reservations)
    result = service._time_conflict(
        table_id=0,
        reservation_time=datetime.now(),
        duration_minutes=15
    )
    assert result is True


def test_time_conflict_False(service):
    reservations = [
        Reservation(
            id=0,
            customer_name="customer_1",
            table_id=0,
            reservation_time=datetime.now() + timedelta(minutes=180),
            duration_minutes=15
        )
    ]

    service.get_all = mock.MagicMock(return_value=reservations)
    result = service._time_conflict(
        table_id=0,
        reservation_time=datetime.now(),
        duration_minutes=15
    )
    assert result is False


def test_add_reservation(service):
    reservations = [
        Reservation(
            id=0,
            customer_name="customer_1",
            table_id=0,
            reservation_time=datetime.now() + timedelta(minutes=180),
            duration_minutes=15
        )
    ]

    service.get_all = mock.MagicMock(return_value=reservations)
    service.add = mock.MagicMock(return_value=reservations)

    result = service.add_reservation(
        customer_name="customer",
        table_id=0,
        reservation_time=datetime.now(),
        duration_minutes=60
    )

    assert result == reservations


def test_add_reservation_wconflict(service):
    reservations = [
        Reservation(
            id=0,
            customer_name="customer_1",
            table_id=0,
            reservation_time=datetime.now() + timedelta(minutes=180),
            duration_minutes=15
        )
    ]

    service.get_all = mock.MagicMock(return_value=reservations)
    service.add = mock.MagicMock(return_value=reservations)

    result = service.add_reservation(
        customer_name="customer",
        table_id=0,
        reservation_time=datetime.now(),
        duration_minutes=60
    )

    assert result == reservations
