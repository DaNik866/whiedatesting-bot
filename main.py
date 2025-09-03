import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

# === Получаем токен из переменной окружения ===
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен бота не задан. Убедитесь, что переменная BOT_TOKEN установлена.")

# === БЛОКИ: ВВОДНЫЕ + ВОПРОСЫ ===
blocks = [
    {
        "intro": {
            "text": (
                "📘 <b>Блок 1: Основы арифметики</b>\n\n"
                "Арифметика — это наука о числах и действиях с ними.\n\n"
                "🔹 <b>Сложение</b>: 2 + 3 = 5\n"
                "🔹 <b>Умножение</b>: 4 × 5 = 20\n"
                "🔹 <b>Порядок действий</b>: сначала умножение и деление, потом — сложение и вычитание."
            ),
            "image_url": "https://i.imgur.com/8Kb9B9L.png"
        },
        "questions": [
            {
                "question": "Сколько будет 5 × 6?",
                "options": ["30", "35", "40"],
                "correct": 0
            },
            {
                "question": "Чему равно 12 + 8 ÷ 4?",
                "options": ["5", "10", "14"],
                "correct": 2
            }
        ]
    },
    {
        "intro": {
            "text": (
                "📘 <b>Блок 2: Строение клетки</b>\n\n"
                "Клетка — основная единица жизни.\n\n"
                "🔹 <b>Ядро</b> — хранит ДНК\n"
                "🔹 <b>Митохондрии</b> — «электростанция» клетки\n"
                "🔹 <b>Цитопласма</b> — жидкость, где происходят реакции"
            ),
            "image_url": "https://i.imgur.com/JpL6FKc.png"
        },
        "questions": [
            {
                "question": "Какой органоид производит энергию?",
                "options": ["Ядро", "Митохондрии", "Лизосома"],
                "correct": 1
            },
            {
                "question": "Где находится ДНК?",
                "options": ["В мембране", "В ядре", "В вакуоли"],
                "correct": 1
            }
        ]
    }
]
# ====================================

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

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
# ================================================

# ============ КЛАВИАТУРА ГЛАВНОГО МЕНЮ ============
def get_main_menu():
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📘 Начать обучение")],
            [types.KeyboardButton(text="ℹ️ О боте"), types.KeyboardButton(text="🛠 Помощь")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard
# ================================================

# ============ ОБРАБОТЧИКИ КНОПОК ============
@dp.message(F.text == "📘 Начать обучение")
async def start_learning(message: types.Message):
    user_data[message.chat.id] = {"current_block": 0}
    await send_block_intro(message.chat.id)

@dp.message(F.text == "ℹ️ О боте")
async def about_bot(message: types.Message):
    text = (
        "📘 <b>Whieda Testing Bot</b>\n\n"
        "Этот бот поможет тебе пройти обучение по разным темам:\n"
        "🔹 Математика\n"
        "🔹 Биология\n"
        "🔹 История и др.\n\n"
        "После каждого блока — интерактивный тест с немедленной обратной связью.\n\n"
        "Разработан для эффективного и удобного самообучения."
    )
    await message.answer(text, parse_mode="HTML", reply_markup=get_main_menu())

@dp.message(F.text == "🛠 Помощь")
async def help_handler(message: types.Message):
    text = (
        "🛠 <b>Помощь</b>\n\n"
        "🔹 Нажми «Начать обучение», чтобы пройти уроки\n"
        "🔹 После каждого блока — тест\n"
        "🔹 После ответа ты сразу увидишь результат\n"
        "🔹 Чтобы вернуться в меню — нажми кнопку ниже\n\n"
        "Если бот не отвечает — напиши /start"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=get_main_menu())
# ================================================

# ============ ОБРАБОТЧИКИ КОМАНД ============
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await show_menu(message)

@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await show_menu(message)
# ================================================

# ============ ПОКАЗ МЕНЮ ============
async def show_menu(message: types.Message):
    text = (
        "👋 <b>Добро пожаловать в Whieda Testing Bot!</b>\n\n"
        "Выбери, что хочешь сделать:"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=get_main_menu())
# ================================================

# ============ ПОКАЗ ВВОДНОГО БЛОКА ============
async
