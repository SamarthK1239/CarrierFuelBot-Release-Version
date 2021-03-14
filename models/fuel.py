from pydantic import BaseModel

# name, fuel_level, reserves, buy order
class FuelIn(BaseModel):
    name: str
    fuel_level: int
    reserves: float
    buy_order: int

class FuelOut(BaseModel):
    id: int
    name: str
    fuel_level: int
    reserves: float
    buy_order: int
