from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["movie_data"]
collection = db["movies_raw"]

movie = {
    "tmdb_id": 550,
    "title": "Fight Club",
    "release_date": "1999-10-15",
    "vote_average": 8.437,
    "vote_count": 32864,
    "runtime": 139,
    "budget": 63000000,
    "revenue": 100853753
}

result = collection.insert_one(movie)

print("Movie inserted successfully!")
print("Document ID:", result.inserted_id)

client.close()