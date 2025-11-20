from aiogram.filters import Filter
from aiogram.types import Message

# Add your admin IDs here
ADMINS = [748108970]


class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS