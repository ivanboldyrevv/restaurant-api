from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Table(BaseModel):
    __tablename__ = "tables"

    name = Column(String)
    seats = Column(Integer)
    location = Column(String)


class Reservation(BaseModel):
    __tablename__ = "reservations"

    customer_name = Column(String(50))
    table_id = Column(Integer, ForeignKey("tables.id"))
    reservation_time = Column(DateTime)
    duration_minutes = Column(Integer)

    table = relationship("Table")
