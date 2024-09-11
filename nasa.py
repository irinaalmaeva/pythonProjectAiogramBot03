import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, NASA_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())  # Используем MemoryStorage для FSM

router = Router()  # Создаем роутер для регистрации хэндлеров


# Функция получения фото дня (APOD)
def get_apod():
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}'
    response = requests.get(url).json()
    return response


# Функция получения информации о погоде на Марсе
def get_mars_weather():
    url = f'https://api.nasa.gov/insight_weather/?api_key={NASA_API_KEY}&feedtype=json&ver=1.0'
    response = requests.get(url).json()
    sol_keys = response.get('sol_keys', [])

    if sol_keys:
        latest_sol = sol_keys[-1]
        weather_data = response[latest_sol]
        temperature = weather_data['AT']['av']
        wind_speed = weather_data['HWS']['av']
        season = weather_data['Season']

        return f"Погода на Марсе (сол {latest_sol}):\nТемпература: {temperature}°C\nСкорость ветра: {wind_speed} м/с\nСезон: {season}"
    return "Нет данных о погоде на Марсе."


# Функция получения информации о ближайших астероидах
def get_neos():
    url = f'https://api.nasa.gov/neo/rest/v1/feed?api_key={NASA_API_KEY}'
    response = requests.get(url).json()
    neos = response['near_earth_objects']
    today_neos = neos[list(neos.keys())[0]]
    message = "Ближайшие к Земле астероиды:\n"
    for neo in today_neos:
        name = neo['name']
        diameter = float(neo['estimated_diameter']['meters']['estimated_diameter_max'])
        miss_distance = float(neo['close_approach_data'][0]['miss_distance']['kilometers'])
        message += f"Имя: {name}, Диаметр: {diameter:.2f} м, Расстояние: {miss_distance:.2f} км\n"
    return message


# Хэндлер для команды /start
@router.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я NASA бот. Вот что я умею:\n"
                         "/apod - Получить фото дня от NASA\n"
                         "/mars_weather - Узнать погоду на Марсе\n"
                         "/neo - Информация о ближайших к Земле астероидах")


# Хэндлер для команды /apod
@router.message(Command(commands=["apod"]))
async def send_apod(message: types.Message):
    data = get_apod()
    if 'url' in data:
        await message.answer_photo(data['url'], caption=data['title'] + '\n' + data.get('explanation', ''))
    else:
        await message.answer("Не удалось получить фото дня.")


# Хэндлер для команды /mars_weather
@router.message(Command(commands=["mars_weather"]))
async def send_mars_weather(message: types.Message):
    weather_info = get_mars_weather()
    await message.answer(weather_info)


# Хэндлер для команды /neo
@router.message(Command(commands=["neo"]))
async def send_neo(message: types.Message):
    neo_info = get_neos()
    await message.answer(neo_info)


# Регистрация роутера в диспетчере
dp.include_router(router)

if __name__ == '__main__':
    dp.run_polling(bot)
