import sqlalchemy

metadata = sqlalchemy.MetaData()

fuels = sqlalchemy.Table(
    "fuels",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(length=30), nullable=False),
    sqlalchemy.Column("fuel_level", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("reserves", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("buy_order", sqlalchemy.Integer, nullable=False),
)
