import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

movie_id = 550

url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "accept": "application/json"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

credits = response.json()

print("Movie ID:", credits["id"])
print("Number of Cast Members:", len(credits["cast"]))

for actor in credits["cast"][:10]:
    print(
        actor["id"],
        "-",
        actor["name"],
        "-",
        actor["character"]
    )