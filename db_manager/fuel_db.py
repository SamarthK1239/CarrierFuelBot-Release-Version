from typing import List

import sqlalchemy
from constants import DATABASE_URL
from models.fuel import FuelIn, FuelOut

from .schemas import FuelTable, metadata


async def create_fuels_table() -> None:
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    
async def get_all_fuels() -> List[FuelOut]:
    fuels = await FuelTable.objects.all()
    return [
        FuelOut(**dict(fuel)) for fuel in fuels
    ]

async def insert_one_fuel(fuel_input: FuelIn) -> FuelOut:
    await FuelTable.objects.create(**fuel_input.dict())

async def delete_one_fuel(fuel_id: int) -> None:
    fuel_to_delete = FuelTable(
        id=fuel_id
    )
    await fuel_to_delete.delete()

async def get_fuels_by_name(name: str) -> List[FuelOut]:
    retrieved_fuels = await FuelTable.objects.filter(name=name).all()
    return retrieved_fuels

async def update_one_fuel(fuel_id: int, fuel_input: FuelIn) -> FuelOut:
    fuel_to_update = FuelTable(
        id=fuel_id,
    )
    await fuel_to_update.update(**fuel_input.dict())
    return FuelOut(
        id=fuel_id,
        **fuel_input.dict(),
    )
