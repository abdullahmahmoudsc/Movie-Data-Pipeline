from pymongo import MongoClient
import pandas as pd


MONGO_URI = "mongodb://localhost:27017"

client = MongoClient(MONGO_URI)

db = client["movie_data"]

collection = db["movies_raw"]


documents = list(collection.find())

df = pd.DataFrame(documents)

print("Raw DataFrame Shape:", df.shape)

# Extract movie details
movie_details_df = pd.json_normalize(df["movie_details"])

print("--------------------------------")
print("Movie Details Shape:", movie_details_df.shape)

print("--------------------------------")
print("Movie Details Columns:")

for column in movie_details_df.columns:
    print(column)

client.close()