import pandas as pd


def transform_data(df):
    # Movie transformation
    movie_details_df = pd.json_normalize(
        df["movie_details"]
    )

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

    movies_df = movie_details_df[
        movie_columns
    ].copy()

    movies_df["release_date"] = pd.to_datetime(
        movies_df["release_date"],
        errors="coerce"
    )


    # Genre transformation
    genres_df = movies_df[
        ["id", "genres"]
    ].copy()

    genres_df = genres_df[
        genres_df["genres"].apply(bool)
    ]

    genres_df = genres_df.explode(
        "genres"
    )

    genres_df["genre_id"] = genres_df[
        "genres"
    ].apply(
        lambda genre: genre["id"]
    )

    genres_df["genre_name"] = genres_df[
        "genres"
    ].apply(
        lambda genre: genre["name"]
    )

    genres_df = genres_df.rename(
        columns={
            "id": "movie_id"
        }
    )

    genres_df = genres_df[
        [
            "movie_id",
            "genre_id",
            "genre_name"
        ]
    ].reset_index(drop=True)


    # Create Genres table
    genres_table = genres_df[
        [
            "genre_id",
            "genre_name"
        ]
    ].drop_duplicates(
        subset=["genre_id"]
    ).reset_index(drop=True)


    # Create Movie_Genres table
    movie_genres_table = genres_df[
        [
            "movie_id",
            "genre_id"
        ]
    ].drop_duplicates(
        subset=[
            "movie_id",
            "genre_id"
        ]
    ).reset_index(drop=True)


    # Actor transformation
    actors_df = df[
        [
            "tmdb_id",
            "credits"
        ]
    ].copy()

    actors_df["cast"] = actors_df[
        "credits"
    ].apply(
        lambda credits: credits.get("cast", [])
        if isinstance(credits, dict)
        else []
    )

    actors_df = actors_df[
        actors_df["cast"].apply(bool)
    ]

    actors_df = actors_df.explode(
        "cast"
    )

    actors_df["actor_id"] = actors_df[
        "cast"
    ].apply(
        lambda actor: actor["id"]
    )

    actors_df["actor_name"] = actors_df[
        "cast"
    ].apply(
        lambda actor: actor["name"]
    )

    actors_df["character"] = actors_df[
        "cast"
    ].apply(
        lambda actor: actor["character"]
    )

    actors_df["cast_order"] = actors_df[
        "cast"
    ].apply(
        lambda actor: actor["order"]
    )

    actors_df = actors_df.rename(
        columns={
            "tmdb_id": "movie_id"
        }
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


    # Create Actors table
    actors_table = actors_df[
        [
            "actor_id",
            "actor_name"
        ]
    ].drop_duplicates(
        subset=["actor_id"]
    ).reset_index(drop=True)


    # Create Movie_Actors table
    movie_actors_table = actors_df[
        [
            "movie_id",
            "actor_id",
            "character",
            "cast_order"
        ]
    ].drop_duplicates(
        subset=[
            "movie_id",
            "actor_id"
        ]
    ).reset_index(drop=True)


    # Prepare Movies table
    movies_table = movies_df.drop(
        columns=["genres"]
    ).rename(
        columns={"id": "movie_id"}
    )


    return {
        "movies": movies_table,
        "actors": actors_table,
        "genres": genres_table,
        "movie_actors": movie_actors_table,
        "movie_genres": movie_genres_table
    }


def validate_data(df, transformed_data):
    movies_df = transformed_data["movies"]
    genres_df = transformed_data["movie_genres"]
    actors_df = transformed_data["movie_actors"]

    movie_details_df = pd.json_normalize(
        df["movie_details"]
    )

    movie_details_df["release_date"] = pd.to_datetime(
        movie_details_df["release_date"],
        errors="coerce"
    )

    missing_values = movie_details_df[
        [
            "id",
            "title",
            "release_date",
            "vote_average",
            "vote_count",
            "popularity",
            "runtime",
            "budget",
            "revenue"
        ]
    ].isnull().sum().sum()

    invalid_dates = movie_details_df[
        "release_date"
    ].isna().sum()

    invalid_vote_average = (
        (movie_details_df["vote_average"] < 0) |
        (movie_details_df["vote_average"] > 10)
    ).sum()

    negative_vote_count = (
        movie_details_df["vote_count"] < 0
    ).sum()

    negative_popularity = (
        movie_details_df["popularity"] < 0
    ).sum()

    negative_runtime = (
        movie_details_df["runtime"] < 0
    ).sum()

    negative_budget = (
        movie_details_df["budget"] < 0
    ).sum()

    negative_revenue = (
        movie_details_df["revenue"] < 0
    ).sum()

    duplicate_movie_ids = (
        movies_df["movie_id"]
        .duplicated()
        .sum()
    )

    invalid_genre_movie_ids = (
        ~genres_df["movie_id"]
        .isin(movies_df["movie_id"])
    ).sum()

    invalid_actor_movie_ids = (
        ~actors_df["movie_id"]
        .isin(movies_df["movie_id"])
    ).sum()

    genre_ids = {
        genre["id"]
        for genres in movie_details_df["genres"]
        for genre in genres
    }

    invalid_genre_ids = (
        ~genres_df["genre_id"]
        .isin(genre_ids)
    ).sum()

    actor_ids = {
        actor["id"]
        for credits in df["credits"]
        for actor in credits.get("cast", [])
    }

    invalid_actor_ids = (
        ~actors_df["actor_id"]
        .isin(actor_ids)
    ).sum()

    validation_results = {
        "Missing values": missing_values,
        "Invalid release dates": invalid_dates,
        "Invalid vote averages": invalid_vote_average,
        "Negative vote counts": negative_vote_count,
        "Negative popularity": negative_popularity,
        "Negative runtimes": negative_runtime,
        "Negative budgets": negative_budget,
        "Negative revenues": negative_revenue,
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

    return validation_results, validation_passed


if __name__ == "__main__":
    from load_from_mongo import load_data

    df = load_data()

    print(f"Raw DataFrame Shape: {df.shape}")

    transformed_data = transform_data(df)

    validation_results, validation_passed = validate_data(
        df,
        transformed_data
    )

    print("\nTransformation Results")
    print(f"Movies: {len(transformed_data['movies'])}")
    print(f"Actors: {len(transformed_data['actors'])}")
    print(f"Genres: {len(transformed_data['genres'])}")
    print(
        f"Movie-Actor relationships: "
        f"{len(transformed_data['movie_actors'])}"
    )
    print(
        f"Movie-Genre relationships: "
        f"{len(transformed_data['movie_genres'])}"
    )

    print("\nValidation Results")

    for check, result in validation_results.items():
        print(f"{check}: {result}")

    if validation_passed:
        print("\nETL Validation: PASSED")
    else:
        print("\nETL Validation: FAILED")