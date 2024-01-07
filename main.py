import logging
from aiogram import Bot, Dispatcher, types

from functions import get_movie_link, get_movie_description
from tokens import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(text="/help")]
    keyboard.add(*buttons)

    await message.answer(
        "Привет! Я бот по поиску фильмов. Просто напиши мне название фильма или сериала, и я постараюсь найти ссылку "
        "для просмотра. Подробнее: /help",
        reply_markup=keyboard
    )


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    help_text = "Доступные команды:\n"
    help_text += "/start - Начать взаимодействие с ботом\n"
    help_text += "/help - Показать список доступных команд\n"
    help_text += "Чтобы найти фильм/сериал и информацию о нём, просто отправьте его название.\n"
    await message.answer(help_text)


@dp.message_handler(content_types=['text'])
async def search_movies(message: types.Message):
    query = message.text
    link = await get_movie_link(query)
    movie_data = await get_movie_description(query)

    if link and movie_data:
        response_text = (
            f"*{movie_data['name']}* | {movie_data['enName']}\n"
            f"\n"
            f"*Тип:* {movie_data['type'].capitalize()}\n"
            f"*Описание:* {movie_data['description']}\n"
            f"\n"
            f"*Статус:* {movie_data['status'].capitalize() if movie_data['isSeries'] and movie_data.get('status') else '-'}\n"
            f"*Жанры:* {', '.join(genre['name'] for genre in movie_data['genres'])}\n"
            f"*Страна выпуска:* {', '.join(country['name'] for country in movie_data['countries'])}\n"
            f"*Год выпуска:* {', '.join(str(year['start']) + '-' + str(year['end']) for year in movie_data['releaseYears']) if movie_data['releaseYears'] else '-'}\n"
            f"\n"
            f"*Где посмотреть:* {link}"
        )
    else:
        response_text = "Извините, ничего не найдено."

    await message.answer(response_text, parse_mode='Markdown')


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
