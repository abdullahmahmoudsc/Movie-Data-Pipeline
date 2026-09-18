import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

movie_id = 550

url = f"https://api.themoviedb.org/3/movie/{movie_id}"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "accept": "application/json"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

movie = response.json()

print("Title:", movie["title"])
print("Release Date:", movie["release_date"])
print("Runtime:", movie["runtime"])
print("Budget:", movie["budget"])
print("Revenue:", movie["revenue"])
print("Genres:", movie["genres"])