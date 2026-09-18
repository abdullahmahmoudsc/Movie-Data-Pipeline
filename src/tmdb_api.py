import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

BASE_URL = "https://api.themoviedb.org/3"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "accept": "application/json"
}


def get_movies(page=1):
    url = f"{BASE_URL}/discover/movie"

    params = {
        "page": page
    }

    response = requests.get(
        url,
        headers=HEADERS,
        params=params
    )

    response.raise_for_status()

    return response.json()


def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"

    response = requests.get(
        url,
        headers=HEADERS
    )

    response.raise_for_status()

    return response.json()


def get_movie_credits(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"

    response = requests.get(
        url,
        headers=HEADERS
    )

    response.raise_for_status()

    return response.json()