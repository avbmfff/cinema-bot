import aiohttp
from bs4 import BeautifulSoup

from tokens import KINOPOISK_API_KEY


async def fetch_movies(query):
    url = f"https://e2.moekino42.net/search?filter=1&query={query.replace(' ', '+')}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_random_movie():
    url = "https://api.kinopoisk.dev/v1.4/movie/random"
    headers = {'accept': 'application/json', 'X-API-KEY': KINOPOISK_API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


async def get_movie_link(query):
    response = await fetch_movies(query)
    soup = BeautifulSoup(response, 'html.parser')
    films = (soup.find('div', attrs={'class': 'film-grid'})
             .findAll("div", attrs={'class': 'film-grid-item'}, recursive=False))

    if not films:
        return None

    link = 'https://e2.moekino42.net'
    path_to_film = films[0].find('a', attrs={'class': 'film-item'})['href']
    return link + path_to_film


async def get_movie_description(query):
    url = f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=1&query={query.replace(' ', '%20')}"
    headers = {'accept': 'application/json', 'X-API-KEY': KINOPOISK_API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            if data['docs']:
                return data['docs'][0]
            else:
                return None
