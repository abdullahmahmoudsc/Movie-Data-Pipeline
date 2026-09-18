import pyodbc
import pandas as pd
import matplotlib.pyplot as plt


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


queries = {
    "movies_per_genre": """
        SELECT
            g.genre_name,
            COUNT(*) AS movie_count
        FROM Movie_Genres mg
        JOIN Genres g
            ON mg.genre_id = g.genre_id
        GROUP BY g.genre_name
        ORDER BY movie_count DESC;
    """,

    "average_rating_per_genre": """
        SELECT
            g.genre_name,
            ROUND(AVG(m.vote_average), 2) AS average_rating
        FROM Movie_Genres mg
        JOIN Movies m
            ON mg.movie_id = m.movie_id
        JOIN Genres g
            ON mg.genre_id = g.genre_id
        GROUP BY g.genre_name
        ORDER BY average_rating DESC;
    """,

    "top_actors": """
        SELECT TOP 10
            a.actor_name,
            COUNT(*) AS movie_count
        FROM Movie_Actors ma
        JOIN Actors a
            ON ma.actor_id = a.actor_id
        GROUP BY a.actor_name
        ORDER BY movie_count DESC;
    """,

    "top_revenue_movies": """
        SELECT TOP 10
            title,
            revenue
        FROM Movies
        WHERE revenue > 0
        ORDER BY revenue DESC;
    """,

    "budget_vs_revenue": """
        SELECT
            title,
            budget,
            revenue
        FROM Movies
        WHERE budget > 0
          AND revenue > 0;
    """
}


movies_per_genre = pd.read_sql(
    queries["movies_per_genre"],
    connection
)

average_rating_per_genre = pd.read_sql(
    queries["average_rating_per_genre"],
    connection
)

top_actors = pd.read_sql(
    queries["top_actors"],
    connection
)

top_revenue_movies = pd.read_sql(
    queries["top_revenue_movies"],
    connection
)

budget_vs_revenue = pd.read_sql(
    queries["budget_vs_revenue"],
    connection
)


connection.close()


plt.figure(figsize=(10, 6))
plt.bar(
    movies_per_genre["genre_name"],
    movies_per_genre["movie_count"]
)
plt.title("Number of Movies per Genre")
plt.xlabel("Genre")
plt.ylabel("Number of Movies")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))
plt.bar(
    average_rating_per_genre["genre_name"],
    average_rating_per_genre["average_rating"]
)
plt.title("Average Movie Rating by Genre")
plt.xlabel("Genre")
plt.ylabel("Average Rating")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))
plt.barh(
    top_actors["actor_name"],
    top_actors["movie_count"]
)
plt.title("Top 10 Actors by Movie Count")
plt.xlabel("Number of Movies")
plt.ylabel("Actor")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))
plt.bar(
    top_revenue_movies["title"],
    top_revenue_movies["revenue"]
)
plt.title("Top 10 Movies by Revenue")
plt.xlabel("Movie")
plt.ylabel("Revenue")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))
plt.scatter(
    budget_vs_revenue["budget"],
    budget_vs_revenue["revenue"]
)
plt.title("Budget vs Revenue")
plt.xlabel("Budget")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()


print("Visualization completed successfully.")