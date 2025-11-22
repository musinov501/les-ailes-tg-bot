"""
Script to insert categories into the database
Usage: python insert_categories.py
"""
import asyncio
from datetime import datetime
from core.database_settings import database
from core.models import categories


async def insert_categories():
    """Insert sample categories"""
    await database.connect()
    
    # Example categories - modify branch_id values to match your branches
    sample_categories = [
        {"name": "Pizza", "branch_id": 1, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Salatlar", "branch_id": 1, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Ichimliklar", "branch_id": 1, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Desertlar", "branch_id": 1, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        # Add more categories for other branches
        {"name": "Pizza", "branch_id": 2, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        {"name": "Salatlar", "branch_id": 2, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
    ]
    
    try:
        for category in sample_categories:
            query = categories.insert().values(**category)
            category_id = await database.execute(query)
            print(f"Inserted category '{category['name']}' (ID: {category_id}) for branch_id {category['branch_id']}")
    except Exception as e:
        print(f"Error inserting categories: {e}")
    finally:
        await database.disconnect()


if __name__ == "__main__":
    asyncio.run(insert_categories())

