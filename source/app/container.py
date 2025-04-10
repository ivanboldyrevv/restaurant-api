from dependency_injector import containers, providers

from app.database import Database

from app.services.table_service import TableService
from app.services.reservation_service import ReservationService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "app.routes.tables", "app.routes.reservations"
    ])
    config = providers.Configuration()

    database = providers.Singleton(
        Database,
        db_uri=config.db.url
    )

    table_service = providers.Factory(
        TableService,
        database=database
    )

    reservation_service = providers.Factory(
        ReservationService,
        database=database
    )
