from app.routes.tables import tables
from app.routes.reservations import reservations
from app.container import Container

from fastapi import FastAPI


def create_app() -> FastAPI:
    container = Container()
    container.config.from_yaml("./app/config.yaml")

    app = FastAPI(
        title="RestaurantAPI"
    )

    app.container = container
    app.include_router(tables, prefix="/tables")
    app.include_router(reservations, prefix="/reservations")

    return app


app = create_app()
