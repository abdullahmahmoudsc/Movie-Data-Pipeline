from pymongo import MongoClient
import pandas as pd


# MongoDB connection
MONGO_URI = "mongodb://localhost:27017"

client = MongoClient(MONGO_URI)
db = client["movie_data"]
collection = db["movies_raw"]


# Load raw data from MongoDB
documents = list(collection.find())
df = pd.DataFrame(documents)

print(f"Raw DataFrame Shape: {df.shape}")


# ============================================================
# Movie Transformation
# ============================================================

movie_details_df = pd.json_normalize(df["movie_details"])

movie_columns = [
    "id",
    "title",
    "original_title",
    "release_date",
    "original_language",
    "overview",
    "vote_average",
    "vote_count",
    "popularity",
    "runtime",
    "budget",
    "revenue",
    "status",
    "tagline",
    "genres"
]

movies_df = movie_details_df[movie_columns].copy()

movies_df["release_date"] = pd.to_datetime(
    movies_df["release_date"],
    errors="coerce"
)

print(f"Movie Data Shape: {movies_df.shape}")


# ============================================================
# Movie Data Validation
# ============================================================

missing_values = movies_df.isnull().sum()

invalid_dates = movies_df["release_date"].isna().sum()

invalid_vote_average = (
    (movies_df["vote_average"] < 0) |
    (movies_df["vote_average"] > 10)
).sum()

negative_vote_count = (movies_df["vote_count"] < 0).sum()
negative_popularity = (movies_df["popularity"] < 0).sum()
negative_runtime = (movies_df["runtime"] < 0).sum()
negative_budget = (movies_df["budget"] < 0).sum()
negative_revenue = (movies_df["revenue"] < 0).sum()

print("\nMovie Data Validation")
print(f"Missing values: {missing_values.sum()}")
print(f"Invalid release dates: {invalid_dates}")
print(f"Invalid vote averages: {invalid_vote_average}")
print(f"Negative vote counts: {negative_vote_count}")
print(f"Negative popularity values: {negative_popularity}")
print(f"Negative runtimes: {negative_runtime}")
print(f"Negative budgets: {negative_budget}")
print(f"Negative revenues: {negative_revenue}")


# ============================================================
# Genre Transformation
# ============================================================

genres_df = movies_df[["id", "genres"]].copy()

movies_without_genres = (
    genres_df["genres"]
    .apply(lambda genres: not genres)
    .sum()
)

genres_df = genres_df[
    genres_df["genres"].apply(bool)
]

genres_df = genres_df.explode("genres")

genres_df["genre_id"] = genres_df["genres"].apply(
    lambda genre: genre["id"]
)

genres_df["genre_name"] = genres_df["genres"].apply(
    lambda genre: genre["name"]
)

genres_df = genres_df.rename(
    columns={"id": "movie_id"}
)

genres_df = genres_df[
    ["movie_id", "genre_id", "genre_name"]
].reset_index(drop=True)

duplicate_genre_relationships = genres_df.duplicated(
    subset=["movie_id", "genre_id"]
).sum()

print("\nGenre Transformation")
print(f"Movies without genres: {movies_without_genres}")
print(f"Movie-Genre relationships: {len(genres_df)}")
print(f"Unique genres: {genres_df['genre_id'].nunique()}")
print(f"Duplicate relationships: {duplicate_genre_relationships}")


# ============================================================
# Actor Transformation
# ============================================================

actors_df = df[["tmdb_id", "credits"]].copy()

actors_df["cast"] = actors_df["credits"].apply(
    lambda credits: credits.get("cast", [])
    if isinstance(credits, dict)
    else []
)

movies_without_cast = (
    actors_df["cast"]
    .apply(lambda cast: not cast)
    .sum()
)

actors_df = actors_df[
    actors_df["cast"].apply(bool)
]

actors_df = actors_df.explode("cast")

actors_df["actor_id"] = actors_df["cast"].apply(
    lambda actor: actor["id"]
)

actors_df["actor_name"] = actors_df["cast"].apply(
    lambda actor: actor["name"]
)

actors_df["character"] = actors_df["cast"].apply(
    lambda actor: actor["character"]
)

actors_df["cast_order"] = actors_df["cast"].apply(
    lambda actor: actor["order"]
)

actors_df = actors_df.rename(
    columns={"tmdb_id": "movie_id"}
)

actors_df = actors_df[
    [
        "movie_id",
        "actor_id",
        "actor_name",
        "character",
        "cast_order"
    ]
].reset_index(drop=True)

duplicate_actor_relationships = actors_df.duplicated(
    subset=["movie_id", "actor_id", "character"]
).sum()

invalid_cast_order = (
    actors_df["cast_order"].isna() |
    (actors_df["cast_order"] < 0)
).sum()

print("\nActor Transformation")
print(f"Movies without cast: {movies_without_cast}")
print(f"Movie-Actor relationships: {len(actors_df)}")
print(f"Unique actors: {actors_df['actor_id'].nunique()}")
print(f"Duplicate relationships: {duplicate_actor_relationships}")
print(f"Invalid cast orders: {invalid_cast_order}")


# ============================================================
# Final ETL Validation
# ============================================================

duplicate_movie_ids = movies_df["id"].duplicated().sum()

invalid_genre_movie_ids = (
    ~genres_df["movie_id"].isin(movies_df["id"])
).sum()

invalid_actor_movie_ids = (
    ~actors_df["movie_id"].isin(movies_df["id"])
).sum()

genre_ids = {
    genre["id"]
    for genres in movies_df["genres"]
    for genre in genres
}

invalid_genre_ids = (
    ~genres_df["genre_id"].isin(genre_ids)
).sum()

actor_ids = {
    actor["id"]
    for credits in df["credits"]
    for actor in credits.get("cast", [])
}

invalid_actor_ids = (
    ~actors_df["actor_id"].isin(actor_ids)
).sum()

validation_results = {
    "Duplicate Movie IDs": duplicate_movie_ids,
    "Invalid Genre Movie IDs": invalid_genre_movie_ids,
    "Invalid Actor Movie IDs": invalid_actor_movie_ids,
    "Invalid Genre IDs": invalid_genre_ids,
    "Invalid Actor IDs": invalid_actor_ids
}

validation_passed = all(
    value == 0
    for value in validation_results.values()
)

print("\nFinal ETL Validation")

for check, result in validation_results.items():
    print(f"{check}: {result}")

print("\nFinal Dataset Sizes")
print(f"Movies: {len(movies_df)}")
print(f"Movie-Genre relationships: {len(genres_df)}")
print(f"Movie-Actor relationships: {len(actors_df)}")
print(f"Unique genres: {genres_df['genre_id'].nunique()}")
print(f"Unique actors: {actors_df['actor_id'].nunique()}")

print("\nETL Status")

if validation_passed:
    print("ETL Validation: PASSED")
else:
    print("ETL Validation: FAILED")


client.close()