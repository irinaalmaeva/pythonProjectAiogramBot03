from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3
import asyncio

# Укажите свой токен
from config import TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Подключение к базе данных и создание таблицы
def create_db():
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            grade TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Сохранение данных в базу данных
def save_to_db(name, age, grade):
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', (name, age, grade))
    conn.commit()
    conn.close()

# Определение машины состояний
class StudentForm(StatesGroup):
    name = State()
    age = State()
    grade = State()

# Хэндлер на команду /start
@dp.message(Command('start'))
async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Привет! Введи своё имя:")
    await state.set_state(StudentForm.name)

# Хэндлер для получения имени
@dp.message(StudentForm.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь введи свой возраст:")
    await state.set_state(StudentForm.age)

# Хэндлер для получения возраста
@dp.message(StudentForm.age)
async def get_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введи корректный возраст:")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Какой у тебя класс (grade)?")
    await state.set_state(StudentForm.grade)

# Хэндлер для получения класса и сохранения данных
@dp.message(StudentForm.grade)
async def get_grade(message: types.Message, state: FSMContext):
    await state.update_data(grade=message.text)
    data = await state.get_data()

    name = data['name']
    age = data['age']
    grade = data['grade']

    # Сохранение данных в базу данных
    save_to_db(name, age, grade)

    await message.answer(f"Спасибо! Данные сохранены:\nИмя: {name}\nВозраст: {age}\nКласс: {grade}")
    await state.clear()  # Очищаем состояние после завершения

# Запуск бота
async def main():
    create_db()  # Создаём базу данных перед запуском
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
