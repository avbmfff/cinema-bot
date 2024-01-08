import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

from functions import get_movie_link, get_movie_description
from tokens import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

conn = sqlite3.connect('movie_bot_db.db')
cursor = conn.cursor()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton(text="/🆘"),
        types.KeyboardButton(text="/🕰"),
        types.KeyboardButton(text="/📊"),
    ]
    keyboard.add(*buttons)

    await message.answer(
        "Привет! Я бот по поиску фильмов. Просто напиши мне название фильма или сериала, и я постараюсь найти ссылку "
        "для просмотра. Подробнее: /help",
        reply_markup=keyboard
    )


@dp.message_handler(lambda message: message.text.lower() in ['/help', '/🆘'])
async def help_command(message: types.Message):
    help_text = "🌟 *Доступные команды:*\n\n"
    help_text += "/start - Начать взаимодействие с ботом\n"
    help_text += "/help - Показать список доступных команд\n"
    help_text += "/history - Показать историю поисковых запросов\n"
    help_text += "/stats - Показать статистику по запросам\n"
    help_text += "\n*Чтобы найти фильм/сериал и информацию о нём, просто отправьте его название.*\n"
    await message.answer(help_text, parse_mode='Markdown')


def create_history_table(user_id):
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS search_history_{user_id} (
            query TEXT,
            search_date TEXT
        )
    ''')


@dp.message_handler(lambda message: message.text.lower() in ['/history', '/🕰'])
async def history_command(message: types.Message):
    user_id = message.from_user.id

    create_history_table(user_id)

    cursor.execute(f'SELECT query, search_date FROM search_history_{user_id}')
    history_entries = cursor.fetchall()

    if history_entries:
        history_text = "🗓 *История поисковых запросов:*\n\n"
        for entry in history_entries:
            history_text += f" __{entry[1]}: {entry[0]}__\n"

        await message.answer(history_text, parse_mode='Markdown')
    else:
        await message.answer("🕰 *История поисковых запросов пуста.*", parse_mode='Markdown')


@dp.message_handler(lambda message: message.text.lower() in ['/stats', '/📊'])
async def stats_command(message: types.Message):
    user_id = message.from_user.id

    create_history_table(user_id)

    cursor.execute(f'SELECT LOWER(query), COUNT(LOWER(query)) FROM search_history_{user_id} GROUP BY LOWER(query)')
    stats_entries = cursor.fetchall()

    if stats_entries:
        stats_text = "📊 *Статистика по запросам:* \n\n"
        for entry in stats_entries:
            stats_text += f"__{entry[0]}: {entry[1]} раз(а)__\n"

        await message.answer(stats_text, parse_mode='Markdown')
    else:
        await message.answer("📊 *Статистика по запросам пуста.*", parse_mode='Markdown')


@dp.message_handler(content_types=['text'])
async def search_movies(message: types.Message):
    query = message.text.upper()
    user_id = message.from_user.id
    create_history_table(user_id)

    link = await get_movie_link(query)
    movie_data = await get_movie_description(query)

    if link and movie_data:
        poster_url = movie_data['poster']['url']
        response_text = (
            f"*{movie_data['name']}* | {movie_data['enName']}\n"
            f"*Рейтинг IMDb:* {movie_data['rating']['imdb']}\n"
            f"\n"
            f"*Тип:* {movie_data['type'].capitalize()}\n"
            f"*Описание:* {movie_data['description']}\n"
            f"\n"
            f"*Статус:* {movie_data['status'].capitalize() if movie_data['isSeries'] and movie_data.get('status') else '-'}\n"
            f"*Жанры:* {', '.join(genre['name'] for genre in movie_data['genres'])}\n"
            f"*Страна выпуска:* {', '.join(country['name'] for country in movie_data['countries'])}\n"
            f"*Год выпуска:* {', '.join(str(year['start']) + '-' + str(year['end']) for year in movie_data['releaseYears']) if movie_data['releaseYears'] else '-'}\n"
        )

        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Перейти к просмотру", url=link)
        keyboard.add(button)

        await bot.send_photo(message.chat.id, poster_url, caption=response_text, parse_mode='Markdown',
                             reply_markup=keyboard)

        cursor.execute(f'INSERT INTO search_history_{user_id} (query, search_date) VALUES (?, datetime("now"))',
                       (query,))
        conn.commit()
    else:
        response_text = "Извините, ничего не найдено."
        await bot.send_message(message.chat.id, response_text)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
