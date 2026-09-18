from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"

client = MongoClient(MONGO_URI)

db = client["movie_data"]

movies_collection = db["movies_raw"]


def insert_movie(movie):
    result = movies_collection.insert_one(movie)
    return result.inserted_id


def close_connection():
    client.close()