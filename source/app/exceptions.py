from datetime import datetime


class CreateReservationException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class NotFoundException(Exception):
    def __init__(self, entity_id: int) -> None:
        super().__init__(
            f"No record found for id: {entity_id}"
        )


class ExistingReservationException(Exception):
    def __init__(self, table_id: int, reservation_time: datetime):
        super().__init__(
            f"the table with id:{table_id} cannot be reserved at "
            f"{reservation_time.strftime('%Y-%m-%d %H:%M')}"
        )
