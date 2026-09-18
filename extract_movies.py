import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

URL = "https://api.themoviedb.org/3/discover/movie"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "accept": "application/json"
}

movies = []

for page in range(1, 6):

    params = {
        "page": page
    }

    response = requests.get(
        URL,
        headers=headers,
        params=params
    )

    print(f"Page {page} - Status Code: {response.status_code}")

    data = response.json()

    movies.extend(data["results"])

print("--------------------------------")

print("Total Movies Collected:", len(movies))

for movie in movies[:10]:
    print(movie["id"], "-", movie["title"])