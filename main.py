print("Этап 1: Импорты выполнены")
import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

print("Этап 1: Импорты выполнены")

# === ТОКЕН БОТА ===
import os
TOKEN = os.getenv("BOT_TOKEN")
print("Этап 2: Токен загружен")

# === БЛОКИ: ВВОДНЫЕ + ВОПРОСЫ ===
blocks = [
    {
        "intro": {
            "text":
            ("?? <b>Блок 1: Основы маркетинга</b>\n\n"
             "Маркетинг — это наука о числах и действиях с ними.\n\n"
             "?? <b>Сложение</b>: 2 + 3 = 5\n"
             "?? <b>Умножение</b>: 4 ? 5 = 20\n"
             "?? <b>Порядок действий</b>: сначала умножение и деление, потом — сложение и вычитание."
             ),
            "image_url":
            "https://i.imgur.com/8Kb9B9L.png"  #  Пробелы удалены
        },
        "questions": [{
            "question": "Сколько будет 5 ? 6?",
            "options": ["30", "35", "40"],
            "correct": 0
        }, {
            "question": "Чему равно 12 + 8 ? 4?",
            "options": ["5", "10", "14"],
            "correct": 2
        }]
    },
    {
        "intro": {
            "text": ("?? <b>Блок 2: Строение клетки</b>\n\n"
                     "Клетка — основная единица жизни.\n\n"
                     "?? <b>Ядро</b> — хранит ДНК\n"
                     "?? <b>Митохондрии</b> — «электростанция» клетки\n"
                     "?? <b>Цитоплазма</b> — жидкость, где происходят реакции"),
            "image_url":
            "https://i.imgur.com/JpL6FKc.png"  #  Пробелы удалены
        },
        "questions": [{
            "question": "Какой органоид производит энергию?",
            "options": ["Ядро", "Митохондрии", "Лизосома"],
            "correct": 1
        }, {
            "question": "Где находится ДНК?",
            "options": ["В мембране", "В ядре", "В вакуоли"],
            "correct": 1
        }]
    }
]
# ====================================

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
print("Этап 3: Бот и диспетчер созданы")
# Хранение данных пользователей
user_data = {}


# ============ МЕНЮ КОМАНД В TELEGRAM ============
async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Начать"),
        types.BotCommand(command="/menu", description="Главное меню"),
        types.BotCommand(command="/help", description="Помощь")
    ]
    await bot.set_my_commands(commands)


print("Этап 4: Команды настроены")

# ================================================


# ============ КЛАВИАТУРА ГЛАВНОГО МЕНЮ ============
def get_main_menu():
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="?? Начать обучение")],
                  [
                      types.KeyboardButton(text="?? О боте"),
                      types.KeyboardButton(text="?? Помощь")
                  ]],
        resize_keyboard=True,
        one_time_keyboard=False)
    return keyboard


# ================================================


# ============ ОБРАБОТЧИКИ КНОПОК ============
@dp.message(F.text == "?? Начать обучение")
async def start_learning(message: types.Message):
    print(f"? {message.from_user.full_name} нажал 'Начать обучение'")
    user_data[message.chat.id] = {"current_block": 0}
    await send_block_intro(message.chat.id)


@dp.message(F.text == "?? О боте")
async def about_bot(message: types.Message):
    text = (
        "?? <b>Whieda Testing Bot</b>\n\n"
        "Этот бот поможет тебе пройти обучение по разным темам:\n"
        "?? Математика\n"
        "?? Биология\n"
        "?? История и др.\n\n"
        "После каждого блока — интерактивный тест с немедленной обратной связью.\n\n"
        "Разработан для эффективного и удобного самообучения.")
    await message.answer(text, parse_mode="HTML", reply_markup=get_main_menu())


@dp.message(F.text == "?? Помощь")
async def help_handler(message: types.Message):
    text = ("?? <b>Помощь</b>\n\n"
            "?? Нажми «Начать обучение», чтобы пройти уроки\n"
            "?? После каждого блока — тест\n"
            "?? После ответа ты сразу увидишь результат\n"
            "?? Чтобы вернуться в меню — нажми кнопку ниже\n\n"
            "Если бот не отвечает — напиши /start")
    await message.answer(text, parse_mode="HTML", reply_markup=get_main_menu())


# ================================================


# ============ ОБРАБОТЧИКИ КОМАНД ============
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    print(f"?? Получено /start от {message.from_user.id}")
    await show_menu(message)


@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await show_menu(message)


# ================================================


# ============ ПОКАЗ МЕНЮ ============
async def show_menu(message: types.Message):
    text = ("?? <b>Добро пожаловать в Whieda Testing Bot!</b>\n\n"
            "Выбери, что хочешь сделать:")
    await message.answer(text, parse_mode="HTML", reply_markup=get_main_menu())


# ================================================


# ============ ПОКАЗ ВВОДНОГО БЛОКА ============
async def send_block_intro(chat_id):
    data = user_data[chat_id]
    block = blocks[data["current_block"]]
    intro = block["intro"]

    try:
        await bot.send_photo(chat_id=chat_id,
                             photo=intro["image_url"],
                             caption=intro["text"],
                             parse_mode="HTML")
    except Exception as e:
        # Если изображение не загрузилось
        await bot.send_message(chat_id=chat_id,
                               text=intro["text"] +
                               "\n\n?? (Изображение недоступно)",
                               parse_mode="HTML")

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="?? Начать тест",
                                 callback_data="start_quiz")
        ],
                         [
                             InlineKeyboardButton(text="?? В главное меню",
                                                  callback_data="main_menu")
                         ]])
    await bot.send_message(chat_id, "Готов пройти тест?", reply_markup=kb)


# ================================================


# ============ ОБРАБОТЧИКИ КНОПОК (инлайн) ============
@dp.callback_query(F.data == "main_menu")
async def go_to_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    await show_menu(callback.message)


@dp.callback_query(F.data == "start_quiz")
async def start_quiz(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    user_data[chat_id]["current_question"] = 0
    await callback.message.edit_reply_markup(reply_markup=None)
    await ask_question(chat_id)


# ================================================


# ============ ОТПРАВКА ВОПРОСОВ ============
async def ask_question(chat_id):
    data = user_data[chat_id]
    block = blocks[data["current_block"]]
    questions = block["questions"]

    if data["current_question"] >= len(questions):
        await bot.send_message(chat_id, "? Блок пройден!")
        data["current_block"] += 1
        if data["current_block"] >= len(blocks):
            await bot.send_message(
                chat_id,
                "?? Поздравляю! Ты прошёл все блоки!\n\nХочешь начать сначала или вернуться в меню?",
                reply_markup=get_main_menu())
        else:
            await asyncio.sleep(1.5)
            await send_block_intro(chat_id)
        return

    q = questions[data["current_question"]]
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for idx, opt in enumerate(q["options"]):
        kb.inline_keyboard.append(
            [InlineKeyboardButton(text=opt, callback_data=f"ans_{idx}")])

    await bot.send_message(chat_id,
                           f"?? Вопрос:\n\n{q['question']}",
                           reply_markup=kb)


# ================================================


# ============ ОБРАБОТКА ОТВЕТОВ ============
@dp.callback_query(F.data.startswith("ans_"))
async def handle_answer(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    user_choice = int(callback.data.split("_")[1])
    data = user_data[chat_id]
    block = blocks[data["current_block"]]
    q = block["questions"][data["current_question"]]

    if user_choice == q["correct"]:
        result = "? Правильно!"
    else:
        correct = q["options"][q["correct"]]
        result = f"? Неверно.\nПравильно: <b>{correct}</b>"

    await callback.message.edit_text(callback.message.text + f"\n\n{result}",
                                     parse_mode="HTML")

    await asyncio.sleep(1.5)
    data["current_question"] += 1
    await ask_question(chat_id)


# ============ ЗАПУСК ============
async def main():
    print("?? 1. Устанавливаем команды...")
    await set_commands(bot)
    print("?? 2. Запускаем polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
