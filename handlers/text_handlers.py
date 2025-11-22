from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.db_commands.branches import get_branches_by_city, get_branch_by_name, get_categories_by_branch
from utils.db_commands.meals import get_meal_info, get_products_by_category

from keyboards.default import (
    language_buttons,
    cities_buttons,
    main_menu_buttons,
    order_buttons,
    pick_up_buttons
)

router = Router()

CITIES = ["Toshkent", "Samarqand", "Andijon", "Farg'ona", "Chirchiq", "Qo'qon"]


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    text = (
        "Assalomu alaykum! Les Ailes yetkazib berish xizmatiga xush kelibsiz.\n\n"
        "Здравствуйте! Добро пожаловать в службу доставки Les Ailes.\n\n"
        "Hello! Welcome to Les Ailes delivery service."
    )
    await message.answer(text=text, reply_markup=language_buttons)

@router.message(F.text == "🇺🇿 Uzbek")
async def uzbek_language_handler(message: Message, state: FSMContext):
    await state.update_data(language="uzbek")
    await message.answer("Qaysi shaharda yashaysiz?\nIltimos shaharni tanlang:", reply_markup=cities_buttons)

@router.message(F.text == "🇷🇺 Russian")
async def russian_language_handler(message: Message, state: FSMContext):
    await state.update_data(language="russian")
    await message.answer("В каком городе вы живете?\nПожалуйста, выберите город:", reply_markup=cities_buttons)

@router.message(F.text == "🇺🇸 English")
async def english_language_handler(message: Message, state: FSMContext):
    await state.update_data(language="english")
    await message.answer("Which city do you live in?\nPlease select a city:", reply_markup=cities_buttons)



@router.message(F.text.in_(CITIES))
async def city_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uzbek")
    city = message.text
    await state.update_data(city=city)

    text = {"uzbek": "Bosh menyu:", "russian": "Главное меню:", "english": "Main Menu:"}[language]
    await message.answer(text=text, reply_markup=main_menu_buttons)


@router.message(F.text == "🛍 Buyurtma berish")
async def order_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uzbek")

    text = {
        "uzbek": "Buyurtmani o'zingiz 🙋‍♂️ olib keting yoki Yetkazib berishni 🚙 tanlang",
        "russian": "Выберите: забрать заказ самостоятельно 🙋‍♂️ или доставку 🚙",
        "english": "Choose: pick up the order yourself 🙋‍♂️ or delivery 🚙"
    }[language]

    await message.answer(text=text, reply_markup=order_buttons)


@router.message(F.text == "🏃 Olib ketish")
async def pick_up_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uzbek")

    text = {
        "uzbek": "Qayerdasiz 👀? Agar lokatsiyangizni📍 yuborsangiz, sizga eng yaqin filialni aniqlaymiz",
        "russian": "Где вы находитесь 👀? Если вы отправите свою локацию📍, мы определим ближайший к вам филиал",
        "english": "Where are you 👀? If you send your location📍, we will determine the nearest branch to you"
    }[language]

    await message.answer(text=text, reply_markup=pick_up_buttons)


@router.message(F.text == "Fillialni tanlang")
async def branches_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    city = user_data.get("city", "Toshkent").strip()

    results = await get_branches_by_city(city=city)
    if not results:
        await message.answer("Bu shaharda filiallar topilmadi. Iltimos boshqa shaharni tanlang.", reply_markup=cities_buttons)
        return

    await state.update_data(branches=[b.name for b in results])
    await state.update_data(branches_obj=results)  

    keyboard = [[KeyboardButton(text=b.name)] for b in results]
    keyboard.append([KeyboardButton(text="🔙 Orqaga")])
    await message.answer("Qaysi filialdan olib ketishni tanlang:", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))


@router.message()
async def menu_flow_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()

    text = message.text

   
    if text == "🔙 Orqaga":
    
        if "meals" in user_data:
          
            categories = user_data.get("categories", [])
            keyboard = [[KeyboardButton(text=c)] for c in categories]
            keyboard.append([KeyboardButton(text="🔙 Orqaga")])
            await message.answer("Nimadan boshlaymiz?", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))
            await state.update_data(meals=None)
            return

        if "categories" in user_data:
           
            branches = user_data.get("branches", [])
            keyboard = [[KeyboardButton(text=b)] for b in branches]
            keyboard.append([KeyboardButton(text="🔙 Orqaga")])
            await message.answer("Qaysi filialdan olib ketishni tanlang:", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))
            await state.update_data(categories=None)
            return

        if "branches" in user_data:
       
            language = user_data.get("language", "uzbek")
            text = {"uzbek": "Bosh menyu:", "russian": "Главное меню:", "english": "Main Menu:"}[language]
            await message.answer(text=text, reply_markup=main_menu_buttons)
            await state.clear()
            return


    if "branches" in user_data and text in user_data["branches"]:
        selected_branch = text
        await state.update_data(selected_branch=selected_branch)

        branch_obj = next((b for b in user_data.get("branches_obj", []) if b.name == selected_branch), None)
        if not branch_obj:
            await message.answer("Filial topilmadi.")
            return

        categories = await get_categories_by_branch(branch_obj.id)
        if not categories:
            await message.answer("Bu filialda menyu yo'q.", reply_markup=main_menu_buttons)
            return

        await state.update_data(categories=[c.name for c in categories])
        await state.update_data(categories_obj=categories)

        keyboard = [[KeyboardButton(text=c.name)] for c in categories]
        keyboard.append([KeyboardButton(text="🔙 Orqaga")])
        await message.answer(f"{selected_branch}\nManzil: {branch_obj.address}\nIsh vaqti: 10:00-22:00\n\nNimadan boshlaymiz?", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))
        return

    if "categories" in user_data and text in user_data["categories"]:
        selected_category_name = text
        category_obj = next((c for c in user_data.get("categories_obj", []) if c.name == selected_category_name), None)
        if not category_obj:
            await message.answer("Bu kategoriya topilmadi.")
            return

        meals = await get_products_by_category(category_obj.id)
        if not meals:
            await message.answer("Bu kategoriyada taomlar topilmadi.")
            return

        await state.update_data(selected_category=selected_category_name)
        await state.update_data(meals=[m.name for m in meals])
        await state.update_data(meals_obj=meals)

        keyboard = [[KeyboardButton(text=m.name)] for m in meals]
        keyboard.append([KeyboardButton(text="🔙 Orqaga")])
        await message.answer("Nimadan boshlaymiz?", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))
        return


    if "meals" in user_data and text in user_data["meals"]:
        meal_obj = next((m for m in user_data.get("meals_obj", []) if m.name == text), None)
        if not meal_obj:
            await message.answer("Bu taom topilmadi.")
            return

        caption = f"🍽 *{meal_obj.name}*\n\n{meal_obj.description}\n\n💰 Narxi: *{meal_obj.price} so'm*"
        back_btn = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🔙 Orqaga")]], resize_keyboard=True)

        if meal_obj.photo_id:
            await message.answer_photo(photo=meal_obj.photo_id, caption=caption, reply_markup=back_btn, parse_mode="Markdown")
        else:
            await message.answer(caption, reply_markup=back_btn, parse_mode="Markdown")
        return
