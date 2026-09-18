import time

from src.tmdb_api import get_movies, get_movie_details, get_movie_credits
from src.mongo import insert_movie, close_connection


def extract_movies(pages=5):
    movies = []

    for page in range(1, pages + 1):

        print(f"\nFetching page {page}...")

        try:
            data = get_movies(page)

        except Exception as e:
            print(f"Failed to fetch page {page}: {e}")
            continue

        for movie in data["results"]:

            movie_id = movie["id"]

            print(f"Fetching movie: {movie_id} - {movie['title']}")

            try:
                details = get_movie_details(movie_id)

                time.sleep(0.3)

                credits = get_movie_credits(movie_id)

                time.sleep(0.3)

                raw_movie = {
                    "tmdb_id": movie_id,
                    "movie_details": details,
                    "credits": credits,
                    "source": "TMDB"
                }

                movies.append(raw_movie)

                print(f"Movie {movie_id} extracted successfully.")

            except Exception as e:
                print(f"Failed to extract movie {movie_id}: {e}")
                continue

    return movies


movies = extract_movies(pages=5)

print("\n--------------------------------")
print("Movies Extracted:", len(movies))
print("--------------------------------")

for movie in movies:
    try:
        insert_movie(movie)
        print(f"Movie {movie['tmdb_id']} inserted into MongoDB.")

    except Exception as e:
        print(f"Failed to insert movie {movie['tmdb_id']}: {e}")

print("--------------------------------")
print("Extraction and MongoDB loading completed!")

close_connection()