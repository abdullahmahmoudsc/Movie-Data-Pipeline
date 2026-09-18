from pymongo import MongoClient
import pandas as pd


MONGO_URI = "mongodb://localhost:27017"

DATABASE_NAME = "movie_data"
COLLECTION_NAME = "movies_raw"


def load_data():

    client = MongoClient(MONGO_URI)

    db = client[DATABASE_NAME]

    collection = db[COLLECTION_NAME]

    documents = list(collection.find())

    df = pd.DataFrame(documents)

    client.close()

    return df


if __name__ == "__main__":

    df = load_data()

    print("Documents Retrieved:", len(df))

    print("--------------------------------")
    print("DataFrame Shape:", df.shape)

    print("--------------------------------")
    print("Columns:")

    for column in df.columns:
        print(column)