from app.services.table_service import TableService
from app.container import Container
from app.schemas.table_schemas import TableCreate, TableRead
from app.exceptions import NotFoundException

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from typing import List, Annotated


tables = APIRouter()


@tables.get("/", response_model=List[TableRead])
@inject
def get_tables(service: Annotated[TableService, Depends(Provide[Container.table_service])]):
    return service.get_all()


@tables.post("/", response_model=TableRead)
@inject
def add_table(table: TableCreate,
              service: Annotated[TableService, Depends(Provide[Container.table_service])]):
    return service.add_table(
        name=table.name,
        seats=table.seats,
        location=table.location
    )


@tables.delete("/{table_id}", status_code=204)
@inject
def delete_table(table_id: int,
                 service: Annotated[TableService, Depends(Provide[Container.table_service])]):
    try:
        service.delete_by_id(table_id)
    except NotFoundException:
        raise HTTPException(status_code=404, detail=f"No record found for id {table_id}!")
