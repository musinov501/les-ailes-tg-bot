import logging
from datetime import datetime
from core.database_settings import database
from core.models import products
from sqlalchemy import and_


async def add_product(data: dict) -> dict | None:
    try:
        query = products.insert().values(
            name=data.get("name"),
            description=data.get("description"),
            price=data.get("price"),
            photo_url=data.get("photo_url"),
            category_id=data.get("category_id"),
            created_at=data.get("created_at", datetime.utcnow()),
            updated_at=data.get("updated_at", datetime.utcnow())
        )
        product_id = await database.execute(query)
        return product_id
    except Exception as e:
        logging.error(f"Error adding product: {e}")
        return None


async def get_products_by_category(category_id: int):
    try:
        query = products.select().where(products.c.category_id == category_id)
        results = await database.fetch_all(query)
        return results
    except Exception as e:
        logging.error(f"Error fetching products for category ID {category_id}: {e}")
        return []


async def get_product_by_name(name: str):
    try:
        query = products.select().where(products.c.name == name)
        product = await database.fetch_one(query)
        return product
    except Exception as e:
        logging.error(f"Error fetching product {name}: {e}")
        return None
