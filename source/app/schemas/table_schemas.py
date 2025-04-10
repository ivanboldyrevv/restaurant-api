from pydantic import BaseModel, PositiveInt


class TableCreate(BaseModel):
    name: str
    seats: PositiveInt
    location: str


class TableRead(TableCreate):
    id: int
