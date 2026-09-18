import pyodbc

from load_from_mongo import load_data
from transform_movies import transform_data


server = "localhost"
database = "MovieDataWarehouse"
driver = "{ODBC Driver 18 for SQL Server}"

connection_string = (
    f"DRIVER={driver};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)


connection = pyodbc.connect(connection_string)
cursor = connection.cursor()


try:
    df = load_data()

    print(f"Loaded {len(df)} raw movies from MongoDB.")

    transformed_data = transform_data(df)

    movies = transformed_data["movies"]
    actors = transformed_data["actors"]
    genres = transformed_data["genres"]
    movie_actors = transformed_data["movie_actors"]
    movie_genres = transformed_data["movie_genres"]

    print("\nTransformation completed.")
    print(f"Movies: {len(movies)}")
    print(f"Actors: {len(actors)}")
    print(f"Genres: {len(genres)}")
    print(f"Movie-Actor relationships: {len(movie_actors)}")
    print(f"Movie-Genre relationships: {len(movie_genres)}")

    # Clear old data before the full reload
    cursor.execute("DELETE FROM Movie_Actors")
    cursor.execute("DELETE FROM Movie_Genres")
    cursor.execute("DELETE FROM Actors")
    cursor.execute("DELETE FROM Genres")
    cursor.execute("DELETE FROM Movies")

    print("\nExisting SQL data cleared.")

    movie_records = list(
        movies.itertuples(index=False, name=None)
    )

    cursor.executemany(
        """
        INSERT INTO Movies (
            movie_id,
            title,
            original_title,
            release_date,
            original_language,
            overview,
            vote_average,
            vote_count,
            popularity,
            runtime,
            budget,
            revenue,
            status,
            tagline
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        movie_records
    )

    print(f"Movies loaded: {len(movie_records)}")

    actor_records = list(
        actors.itertuples(index=False, name=None)
    )

    cursor.executemany(
        """
        INSERT INTO Actors (
            actor_id,
            actor_name
        )
        VALUES (?, ?)
        """,
        actor_records
    )

    print(f"Actors loaded: {len(actor_records)}")

    genre_records = list(
        genres.itertuples(index=False, name=None)
    )

    cursor.executemany(
        """
        INSERT INTO Genres (
            genre_id,
            genre_name
        )
        VALUES (?, ?)
        """,
        genre_records
    )

    print(f"Genres loaded: {len(genre_records)}")

    movie_actor_records = list(
        movie_actors.itertuples(index=False, name=None)
    )

    cursor.executemany(
        """
        INSERT INTO Movie_Actors (
            movie_id,
            actor_id,
            character,
            cast_order
        )
        VALUES (?, ?, ?, ?)
        """,
        movie_actor_records
    )

    print(
        f"Movie-Actor relationships loaded: "
        f"{len(movie_actor_records)}"
    )

    movie_genre_records = list(
        movie_genres.itertuples(index=False, name=None)
    )

    cursor.executemany(
        """
        INSERT INTO Movie_Genres (
            movie_id,
            genre_id
        )
        VALUES (?, ?)
        """,
        movie_genre_records
    )

    print(
        f"Movie-Genre relationships loaded: "
        f"{len(movie_genre_records)}"
    )

    connection.commit()

    print("\nSQL Server load completed successfully.")


except Exception as e:
    connection.rollback()
    print(f"\nSQL Server load failed: {e}")


finally:
    cursor.close()
    connection.close()