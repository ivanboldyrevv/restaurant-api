from datetime import datetime, timedelta

from app.services.service import BaseService
from app.database import Database
from app.models import Reservation
from app.exceptions import ExistingReservationException, CreateReservationException

from sqlalchemy.exc import IntegrityError


class ReservationService(BaseService):
    def __init__(self, database: Database):
        super().__init__(database, Reservation)

    def add_reservation(self,
                        customer_name: str,
                        table_id: int,
                        reservation_time: datetime,
                        duration_minutes: int) -> Reservation:
        if self._time_conflict(table_id, reservation_time, duration_minutes):
            raise ExistingReservationException(table_id, reservation_time)
        try:
            return self.add(
                Reservation(
                    customer_name=customer_name,
                    table_id=table_id,
                    reservation_time=reservation_time,
                    duration_minutes=duration_minutes
                )
            )
        except IntegrityError:
            raise CreateReservationException(
                f"Failed to create reservation. No table with id {table_id} exists"
            )

    def _time_conflict(self,
                       table_id: int,
                       reservation_time: datetime,
                       duration_minutes: int) -> bool:
        reserved_tables = self.get_all()

        def overlaps(entity: Reservation) -> bool:
            start_time = reservation_time.replace(tzinfo=None)
            end_time = start_time + timedelta(minutes=duration_minutes)
            return (
                entity.table_id == table_id and
                entity.reservation_time <= end_time and
                entity.reservation_time + timedelta(minutes=entity.duration_minutes) >= start_time
            )

        return any(overlaps(entity) for entity in reserved_tables)
