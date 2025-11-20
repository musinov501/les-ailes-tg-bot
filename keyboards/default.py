from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language_buttons = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="🇺🇿 Uzbek"),
            KeyboardButton(text="🇷🇺 Russian"),
            KeyboardButton(text="🇺🇸 English"),
        ]
    ],
    resize_keyboard=True
)

cities_buttons = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="Toshkent"),
            KeyboardButton(text="Samarqand"),
        ],
        [
            KeyboardButton(text="Andijon"),
            KeyboardButton(text="Farg'ona"),
        ],
        [
            KeyboardButton(text="Chirchiq"),
            KeyboardButton(text="Qo'qon"),

        ],
    ]
)

main_menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛍 Buyurtma berish")
        ],
        [
            KeyboardButton(text="📖 Buyurtmalar tarixi")
        ],
        [
            KeyboardButton(text="⚙Sozlashℹ️Ma'lumotlar"),
            KeyboardButton(text="🔥Aksiya")
        ],
        [
        KeyboardButton(text="🙋🏻‍♂️ Jamoamizga qo'shiling"),
        KeyboardButton(text="☎️ Les Ailes bilan aloqa")
        ]
    ], resize_keyboard=True
)

order_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🏃 Olib ketish"),
            KeyboardButton(text="🚙 Yetkazib berish")
        ],
        [
            KeyboardButton(text="🔙 Orqaga")
        ]
    ], resize_keyboard=True
)

pick_up_buttons = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="🔙 Orqaga"),
            KeyboardButton(text="📍eng yaqin fillialni aniqlash")
        ],
        [
            KeyboardButton(text="Bu yerda buyurtma berish🌐"),
            KeyboardButton(text="Fillialni tanlang")
        ]
    ], resize_keyboard=True
)

