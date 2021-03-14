from sqlalchemy.sql.dml import Update
from db_manager.db_utilities import build_query
from typing import List
from models.fuel import FuelIn, FuelOut
from .schemas import fuels
from .db_connector import db
from sqlalchemy.schema import CreateTable

async def create_fuels_table() -> None:
    sql_statement = str(CreateTable(fuels))
    await db.execute(sql_statement)

async def get_fuels(query: str, values=None) -> List[FuelOut]:
    mapped_fuels: List[FuelOut] = []
    async for row in db.iterate(query=query, values=values):
        mapped_fuels.append(FuelOut(
            id=row[0],
            name=str(row[1]),
            fuel_level=int(row[2]),
            reserves=float(row[3]),
            buy_order=int(row[4]),
        ))
    return mapped_fuels

async def get_all_fuels() -> List[FuelOut]:
    query = str(fuels.select())
    retrieved_fuels = await get_fuels(query)
    return retrieved_fuels

async def insert_one_fuel(fuel_input: FuelIn) -> FuelOut:
    query = fuels.insert()
    fuel_id: int = await db.execute(query=query, values=fuel_input.dict())
    return FuelOut(**{
        **fuel_input.dict(),
        'id': fuel_id
    })

async def delete_one_fuel(fuel_id: int) -> None:
    query, values = build_query(fuels, 'delete', filters={
        'equalTo': {
            'id': int(fuel_id)
        }
    })
    await db.execute(query=query, values=values)

async def update_one_fuel(fuel_input: FuelIn) -> FuelOut:
    query: Update = None
    query, values = build_query(fuels, 'update', filters={
        'equalTo': {
            'name': str(fuel_input.name),
        }
    })
    query = query.values(
        name = '',
        fuel_level='',
        reserves = '',
        buy_order=''
    )
    values = {
        **values,
        **fuel_input.dict()
    }
    fuel_id: int = await db.execute(query=str(query), values=values)
    return FuelOut(**{
        **fuel_input.dict(),
        'id': fuel_id
    })
