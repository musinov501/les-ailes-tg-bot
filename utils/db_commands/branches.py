import logging
from datetime import datetime
from core.database_settings import database
from core.models import branches
from sqlalchemy import and_, func
from core.models import categories



async def add_branch(data: dict) -> dict | None:
    try:
        query = branches.insert().values(
            name = data.get("name"),
            city = data.get("city"),
            address = data.get("address"),
            created_at = data.get("created_at", datetime.utcnow()),
            updated_at = data.get("updated_at", datetime.utcnow())
        )
        branch_id = await database.execute(query)
        return branch_id
    except Exception as e:
        logging.error(f"Error adding branch: {e}")
        return None
    
    
async def get_branches_by_city(city: str) -> list:
  
    try:
        city_clean = city.strip().lower()
        query = branches.select().where(
            func.lower(func.trim(branches.c.city)) == city_clean
        )
        results = await database.fetch_all(query)
        return results
    except Exception as e:
        logging.error(f"Error fetching branches for city '{city}': {e}")
        return []
    
async def get_branch_by_name(city: str, branch_name: str) -> dict | None:
    
    try:
        query = branches.select().where(
            and_(
                branches.c.city == city,
                branches.c.name == branch_name
            )
        )
        branch = await database.fetch_one(query)
        return branch
    except Exception as e:
        logging.error(f"Error fetching branch {branch_name} in city {city}: {e}")
        return None
    
   
async def get_categories_by_branch(branch_id: int):
    try:
        query = categories.select().where(categories.c.branch_id == branch_id)
        results = await database.fetch_all(query)
        return results
    except Exception as e:
        logging.error(f"Error fetching categories for branch ID {branch_id}: {e}")
        return []
