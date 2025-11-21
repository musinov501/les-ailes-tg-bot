import sqlalchemy
from sqlalchemy import DateTime, Integer, String, BigInteger, SmallInteger, Column, Boolean, ForeignKey
from core.database_settings import metadata


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", Integer, primary_key=True),
    sqlalchemy.Column("full_name", String),
    sqlalchemy.Column("language", String),
    sqlalchemy.Column("age", SmallInteger),
    sqlalchemy.Column("chat_id", BigInteger, unique=True),
    sqlalchemy.Column("phone_number", String),
    sqlalchemy.Column("created_at", DateTime(timezone=True), nullable=True),
    sqlalchemy.Column("updated_at", DateTime(timezone=True), nullable=True)
    
)


categories = sqlalchemy.Table(
    "categories",
    metadata,
    sqlalchemy.Column("id", Integer, primary_key=True),
    sqlalchemy.Column("name", String, unique=True),
    sqlalchemy.Column("created_at", DateTime(timezone=True)),
    sqlalchemy.Column("updated_at", DateTime(timezone=True))
)



products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", Integer, primary_key=True),
    sqlalchemy.Column("name", String),
    sqlalchemy.Column("price", Integer),
    sqlalchemy.Column("category_id", Integer, ForeignKey("categories.id")),
    sqlalchemy.Column("description", String),
    sqlalchemy.Column("photo_id", String),
    sqlalchemy.Column("created_at", DateTime(timezone=True)),
    sqlalchemy.Column("updated_at", DateTime(timezone=True)),
)



orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", Integer, primary_key=True),
    sqlalchemy.Column("user_id", Integer, ForeignKey("users.id")),
    sqlalchemy.Column("total_price", Integer),
    sqlalchemy.Column("status", String),
    sqlalchemy.Column("created_at", DateTime(timezone=True)),
)


branches = sqlalchemy.Table(
    "branches",
    metadata,
    sqlalchemy.Column("id", Integer, primary_key=True),
    sqlalchemy.Column("name", String),
    sqlalchemy.Column("city", String),
    sqlalchemy.Column("address", String),
    sqlalchemy.Column("created_at", DateTime(timezone=True)),
    sqlalchemy.Column("updated_at", DateTime(timezone=True)),
)









