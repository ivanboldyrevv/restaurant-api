from app.services.reservation_service import ReservationService
from app.container import Container
from app.schemas.reservation_schemas import ReservationCreate, ReservationRead
from app.exceptions import (NotFoundException,
                            ExistingReservationException,
                            CreateReservationException)

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from typing import List, Annotated


reservations = APIRouter()


@reservations.get("/", response_model=List[ReservationRead])
@inject
def get_reservations(service: Annotated[ReservationService, Depends(Provide[Container.reservation_service])]):
    return service.get_all()


@reservations.post("/", response_model=ReservationRead)
@inject
def add_reservation(reservation: ReservationCreate,
                    service: Annotated[ReservationService, Depends(Provide[Container.reservation_service])]):
    try:
        return service.add_reservation(
            customer_name=reservation.customer_name,
            table_id=reservation.table_id,
            reservation_time=reservation.reservation_time,
            duration_minutes=reservation.duration_minutes
        )
    except CreateReservationException:
        raise HTTPException(status_code=409,
                            detail=f"Failed to create reservation. No table with id {reservation.table_id} exists")
    except ExistingReservationException:
        raise HTTPException(status_code=409, detail="The table for this time is already reserved!")


@reservations.delete("/{reservation_id}", status_code=204)
@inject
def delete_reservation(reservation_id: int,
                       service: Annotated[ReservationService, Depends(Provide[Container.reservation_service])]):
    try:
        service.delete_by_id(reservation_id)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=f"No record found for id {reservation_id}!")
