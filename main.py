from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import sqlite3
import asyncio

from config import TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для сохранения данных в базу данных
def save_to_db(name, age, grade):
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', (name, age, grade))
    conn.commit()
    conn.close()

# Хэндлер на команду /start
@dp.message(CommandStart())
async def start(message: Message, state):
    await message.answer("Привет! Введи своё имя:")
    await state.set_data({'stage': 'name'})

# Обработка имени
@dp.message(F.text, state=lambda state: state.data.get('stage') == 'name')
async def get_name(message: Message, state):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Теперь введи свой возраст:")
    await state.update_data(stage='age')

# Обработка возраста
@dp.message(F.text, state=lambda state: state.data.get('stage') == 'age')
async def get_age(message: Message, state):
    if message.text.isdigit():
        age = int(message.text)
        await state.update_data(age=age)
        await message.answer("Какой у тебя класс (grade)?")
        await state.update_data(stage='grade')
    else:
        await message.answer("Пожалуйста, введи корректный возраст!")

# Обработка класса и сохранение данных
@dp.message(F.text, state=lambda state: state.data.get('stage') == 'grade')
async def get_grade(message: Message, state):
    grade = message.text
    data = await state.get_data()

    name = data['name']
    age = data['age']

    # Сохранение данных в базу данных
    save_to_db(name, age, grade)

    await message.answer(f"Спасибо! Данные сохранены:\nИмя: {name}\nВозраст: {age}\nКласс: {grade}")
    await state.clear()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
