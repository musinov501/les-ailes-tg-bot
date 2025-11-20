import logging

from core.database_settings import database
from core.models import users

async def add_user(data: dict) -> dict | None:
    try:
        query = users.insert().values(
            full_name=data.get("full_name"),
            phone_number=data.get("phone_number"),
            chat_id=data.get("chat_id"),
            age=int(data.get("age")),
            language=data.get("language"),
            created_at=data.get("created_at"),
            updated_at=data.get("created_at")
        )
        new_user = await database.execute(query=query)
        return new_user
    except Exception as e:
        error_text = f"Error appeared when getting user: {e}"
        logging.error(error_text)
        return None
    

async def get_user(chat_id: int) -> dict | None:
    try:
        query = users.select().where(users.c.chat.id == chat_id)
        user = await database.fetch_one(query)
        return user
    except Exception as e:
        logging.error(f"Error fetching user with chat_id {chat_id}: {e}")
        return None
    


