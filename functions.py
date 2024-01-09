import aiohttp
import httpx
from bs4 import BeautifulSoup
from typing import Optional, List, Dict, Any

from tokens import KINOPOISK_API_KEY


async def get_random_movie() -> Dict[str, Any]:
    url = "https://api.kinopoisk.dev/v1.4/movie/random"
    headers = {'accept': 'application/json', 'X-API-KEY': KINOPOISK_API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


async def get_movie_description(query: str) -> Optional[Dict[str, Any]]:
    url = f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=1&query={query.replace(' ', '%20')}"
    headers = {'accept': 'application/json', 'X-API-KEY': KINOPOISK_API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            if data['docs']:
                return data['docs'][0]
            else:
                return None


async def fetch_movies(query: str) -> str:
    url = f"https://e2.moekino42.net/search?filter=1&query={query.replace(' ', '+')}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text


async def parse_movies(response_text: str) -> List[BeautifulSoup]:
    soup = BeautifulSoup(response_text, 'html.parser')
    films = (soup.find('div', attrs={'class': 'film-grid'})
             .findAll("div", attrs={'class': 'film-grid-item'}, recursive=False))

    return films


async def get_movie_link(query: str) -> Optional[str]:
    response_text = await fetch_movies(query)
    films = await parse_movies(response_text)

    if not films:
        return None

    link = 'https://e2.moekino42.net'
    path_to_film = films[0].find('a', attrs={'class': 'film-item'})['href']
    return link + path_to_film
