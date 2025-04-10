from datetime import datetime
from pydantic import BaseModel, PositiveInt


class ReservationCreate(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: PositiveInt


class ReservationRead(ReservationCreate):
    id: int
