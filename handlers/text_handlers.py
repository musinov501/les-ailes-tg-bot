from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from core.models import branches as branches_db
from utils.db_commands.branches import get_branches_by_city
from core.database_settings import database
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from keyboards.default import (language_buttons, 
                               cities_buttons, 
                               main_menu_buttons, 
                               order_buttons,
                               pick_up_buttons
                               )




router = Router()


CITIES = ["Toshkent", "Samarqand", "Andijon", "Farg'ona", "Chirchiq", "Qo'qon"]

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    text = "Assalomu alaykum! Les Ailes yetkazib berish xizmatiga xush kelibsiz.\n\nЗдравствуйте! Добро пожаловать в службу доставки Les Ailes.\n\nHello! Welcome to Les Ailes delivery service."
    await message.answer(text=text, reply_markup=language_buttons)


@router.message(F.text == "🇺🇿 Uzbek")
async def uzbek_language_handler(message: Message, state: FSMContext):
    await state.update_data(language="uzbek")
    text = "Qaysi shaharda yashaysiz?\nIltimos shaharni tanlang:"
    await message.answer(text=text, reply_markup=cities_buttons)


@router.message(F.text == "🇷🇺 Russian")
async def russian_language_handler(message: Message, state: FSMContext):
    await state.update_data(language="russian")
    text = "В каком городе вы живете?\nПожалуйста, выберите город:"
    await message.answer(text=text, reply_markup=cities_buttons)


@router.message(F.text == "🇺🇸 English")
async def english_language_handler(message: Message, state: FSMContext):
    await state.update_data(language="english")
    text = "Which city do you live in?\nPlease select a city:"
    await message.answer(text=text, reply_markup=cities_buttons)
    

@router.message(F.text.in_(CITIES))
async def city_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uzbek")

    city = message.text
    await state.update_data(city=city)

    if language == "uzbek":
        text = f"Bosh menyu:"
    elif language == "russian":
        text = f"Главное меню:"
    else:
        text = f"Main Menu:"
        
    await message.answer(text=text, reply_markup=main_menu_buttons)
    
    
@router.message(F.text == "🛍 Buyurtma berish")
async def order_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uzbek")

    if language == "uzbek":
        text = "Buyurtmani o'zingiz 🙋‍♂️ olib keting yoki Yetkazib berishni 🚙 tanlang"
    elif language == "russian":
        text = "Выберите: забрать заказ самостоятельно 🙋‍♂️ или доставку 🚙"
    else:
        text = "Choose: pick up the order yourself 🙋‍♂️ or delivery 🚙"

    await message.answer(text=text, reply_markup=order_buttons)
    
@router.message(F.text == "🔙 Orqaga")
async def back_to_main_menu_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uzbek")

    if language == "uzbek":
        text = f"Bosh menyu:"
    elif language == "russian":
        text = f"Главное меню:"
    else:
        text = f"Main Menu:"
        
    await message.answer(text=text, reply_markup=main_menu_buttons)
    
    
@router.message(F.text == "🏃 Olib ketish")
async def pick_up_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uzbek")

    if language == "uzbek":
        text = "Qayerdasiz 👀? Agar lokatsiyangizni📍 yuborsangiz, sizga eng yaqin filialni aniqlaymiz"
    elif language == "russian":
        text = "Где вы находитесь 👀? Если вы отправите свою локацию📍, мы определим ближайший к вам филиал"
    else:
        text = "Where are you 👀? If you send your location📍, we will determine the nearest branch to you"

    await message.answer(text=text, reply_markup=pick_up_buttons)
    
    
@router.message(F.text == "Fillialni tanlang")
async def branches_handler(message: Message, state: FSMContext):
    user_data  = await state.get_data()
    city = user_data.get("city", "Toshkent").strip()
    
    
    print("🔥 CITY FROM FSM =", repr(city))
    
    results = await get_branches_by_city(city=city)
    
    if not results:
        await message.answer(text="Bu shaharda filiallar topilmadi. Iltimos boshqa shaharni tanlang.", reply_markup=cities_buttons)
        return
    
    await state.update_data(branches = [b.name for b in results])
    
    keyboard = []
    for branch in results:
        keyboard.append([KeyboardButton(text=branch.name)])
    keyboard.append([KeyboardButton(text="🔙 Orqaga")])
    
    branch_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    
    await message.answer(text = "Qaysi filialdan olib ketishni tanlang:", reply_markup=branch_keyboard)
    
    



    
    

