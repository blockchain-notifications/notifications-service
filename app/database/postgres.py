import sqlalchemy

from app.config import DATABASE_URL

metadata = sqlalchemy.MetaData()

notifications = sqlalchemy.Table(
    "notifications",
    metadata,
    sqlalchemy.Column("tx_hash", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("recipient", sqlalchemy.String),
    sqlalchemy.Column("sender", sqlalchemy.String),
    sqlalchemy.Column("data", sqlalchemy.String),
    sqlalchemy.Column("event", sqlalchemy.String),
    sqlalchemy.Column("is_read", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL,
)

metadata.create_all(engine)
