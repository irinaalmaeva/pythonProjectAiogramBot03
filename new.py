from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from aiogram import F




from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Задание 1: Команда /start - меню с кнопками "Привет" и "Пока"
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
        ],
        resize_keyboard=True
    )

    await message.answer("Выберите опцию:", reply_markup=keyboard)


@dp.message(lambda message: message.text == "Привет")
async def greet_user(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(f"Привет, {user_name}!")


@dp.message(lambda message: message.text == "Пока")
async def say_goodbye(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(f"До свидания, {user_name}!")


# Задание 2: Команда /links - инлайн-кнопки с URL-ссылками

@dp.message(Command("links"))
async def send_links(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Новости", url="https://www.bbc.com/news")],
            [InlineKeyboardButton(text="Музыка", url="https://tunein.com/music/")],
            [InlineKeyboardButton(text="Видео", url="https://www.youtube.com")]
        ]
    )

    await message.answer("Вот несколько полезных ссылок:", reply_markup=keyboard)


# Задание 3: Команда /dynamic - динамическое изменение клавиатуры
# Команда для динамической клавиатуры
@dp.message(Command("dynamic"))
async def dynamic_keyboard(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ])
    await message.answer("Выберите действие:", reply_markup=keyboard)

# Обработка нажатия на кнопку
@dp.callback_query(F.data == "show_more")
async def show_more_options(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
    ])
    await callback.message.edit_text("Выберите опцию:", reply_markup=keyboard)

# Обработка выбора опций
@dp.callback_query(F.data.in_({"option_1", "option_2"}))
async def option_selected(callback: types.CallbackQuery):
    option = "Опция 1" if callback.data == "option_1" else "Опция 2"
    await callback.message.edit_text(f"Вы выбрали: {option}")

# Основная функция для запуска бота
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
