import sqlalchemy
import orm
from .db_connector import db

metadata = sqlalchemy.MetaData()

class FuelTable(orm.Model):
    __tablename__ = "fuels"
    __database__ = db
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    name = orm.String(max_length=30)
    fuel_level = orm.Integer(minimum=0, maximum=100)
    reserves = orm.Float()
    buy_order = orm.Boolean()
    guild_id = orm.Integer()
