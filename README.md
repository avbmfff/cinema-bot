# Movie Search Bot Documentation

## Introduction
This bot is designed to help users find information about movies and TV series, as well as provide links for streaming. Users can interact with the bot by sending the name of a movie or TV series as a message. The bot will then search for the requested content and provide relevant details.

## Getting Started
To start interacting with the bot, use the `/start` command. The bot will respond with a set of commands and instructions on how to use them.

### Commands
- `/start`: Begin interaction with the bot.
- `/help` or `/🆘`: Display a list of available commands and brief instructions.
- `/history` or `/🕰`: View the history of search queries.
- `/stats` or `/📊`: Display statistics on search queries.

## Features
### 1. Movie/TV Series Search
To find information about a specific movie or TV series, simply send the name of the content as a text message. The bot will respond with details such as the title, IMDb rating, description, type, status, genres, country of release, and release year. The poster's description is obtained using the [Kinopoisk API](https://api.kinopoisk.dev/documentation#/%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B%2C%20%D1%81%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%2C%20%D0%B8%20%D1%82.%D0%B4./MovieController_searchMovieV1_4).

### 2. Search History
The bot keeps track of the search history for each user. Users can use the `/history` command to view their past search queries along with the corresponding dates.

### 3. Search Statistics
The `/stats` command provides users with statistics on their search queries. It shows how many times a particular query has been searched.

## Example Usage
1. **Start the Interaction:**
   - Send the `/start` command to initiate interaction with the bot.

2. **Search for a Movie:**
   - Send the name of a movie or TV series as a text message.
   - Example: "Inception" or "Game of Thrones."

3. **View Search History:**
   - Use the `/history` command to see a list of past search queries.

4. **View Search Statistics:**
   - Use the `/stats` command to see statistics on the frequency of each search query.

## Technical Details
The bot is implemented in Python using the `aiogram` library for Telegram bot development. It also uses SQLite for storing user-specific search history. The search for movie information is powered by the Kinopoisk API, and the link for streaming is obtained through web scraping using `aiohttp` and `BeautifulSoup`.

### Poster Description
The poster's description is obtained using the [Kinopoisk API](https://api.kinopoisk.dev/documentation#/%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B%2C%20%D1%81%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%2C%20%D0%B8%20%D1%82.%D0%B4./MovieController_searchMovieV1_4). The API provides additional details about the movie or TV series, including the poster's URL.

### Link Extraction
The streaming link is obtained by scraping the website [moekino42.net](https://e2.moekino42.net). The bot utilizes web scraping techniques with `aiohttp` and `BeautifulSoup` to find the link for streaming. The first available film's link is extracted from the website's HTML structure.

## Dependencies
- `aiogram`: Telegram bot development library.
- `aiohttp`: Asynchronous HTTP client.
- `BeautifulSoup`: Web scraping library.
- `sqlite3`: SQLite database for storing search history.

## Installation
1. Install the required dependencies using the following command:
   ```bash
   pip install aiogram aiohttp beautifulsoup4

2. Create a Telegram bot and obtain the API token with [@BotFather](https://telegram.me/BotFather)

3. Obtain a [Kinopoisk API](https://kinopoisk.dev/) key.

4. Create a file named tokens.py and define the following variables:
   ```python
   API_TOKEN = "YOUR_TELEGRAM_BOT_API_TOKEN"
   KINOPOISK_API_KEY = "YOUR_KINOPOISK_API_KEY"

5. Run the provided Python script to start the bot:
    ```python
   python main.py

## Note
Ensure that your bot has the necessary permissions and privacy settings to receive and process messages.

Feel free to explore and modify the code to suit your specific requirements. Happy movie searching!