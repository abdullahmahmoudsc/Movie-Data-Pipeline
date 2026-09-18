from pymongo import MongoClient
import pandas as pd


MONGO_URI = "mongodb://localhost:27017"

client = MongoClient(MONGO_URI)

db = client["movie_data"]

collection = db["movies_raw"]


documents = list(collection.find())

print("Documents Retrieved:", len(documents))

df = pd.DataFrame(documents)

print("--------------------------------")
print("DataFrame Shape:", df.shape)

print("--------------------------------")
print("Columns:")

for column in df.columns:
    print(column)

client.close()