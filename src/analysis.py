import pyodbc


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


queries = {
    "Highest Rated Movies": """
        SELECT TOP 10
            movie_id,
            title,
            vote_average,
            vote_count
        FROM Movies
        WHERE vote_count >= 100
        ORDER BY vote_average DESC, vote_count DESC;
    """,

    "Most Voted Movies": """
        SELECT TOP 10
            movie_id,
            title,
            vote_count,
            vote_average
        FROM Movies
        ORDER BY vote_count DESC;
    """,

    "Most Popular Movies": """
        SELECT TOP 10
            movie_id,
            title,
            popularity,
            vote_average
        FROM Movies
        ORDER BY popularity DESC;
    """,

    "Movies per Genre": """
        SELECT
            g.genre_name,
            COUNT(*) AS movie_count
        FROM Movie_Genres mg
        JOIN Genres g
            ON mg.genre_id = g.genre_id
        GROUP BY g.genre_name
        ORDER BY movie_count DESC;
    """,

    "Average Rating per Genre": """
        SELECT
            g.genre_name,
            COUNT(*) AS movie_count,
            ROUND(AVG(m.vote_average), 2) AS average_rating
        FROM Movie_Genres mg
        JOIN Movies m
            ON mg.movie_id = m.movie_id
        JOIN Genres g
            ON mg.genre_id = g.genre_id
        GROUP BY g.genre_name
        ORDER BY average_rating DESC;
    """,

    "Top Actors by Movie Count": """
        SELECT TOP 10
            a.actor_name,
            COUNT(*) AS movie_count
        FROM Movie_Actors ma
        JOIN Actors a
            ON ma.actor_id = a.actor_id
        GROUP BY a.actor_name
        ORDER BY movie_count DESC;
    """,

    "Highest Revenue Movies": """
        SELECT TOP 10
            movie_id,
            title,
            budget,
            revenue
        FROM Movies
        WHERE revenue > 0
        ORDER BY revenue DESC;
    """,

    "Budget vs Revenue": """
        SELECT TOP 10
            title,
            budget,
            revenue,
            revenue - budget AS profit
        FROM Movies
        WHERE budget > 0
          AND revenue > 0
        ORDER BY profit DESC;
    """
}


for name, query in queries.items():
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    cursor.execute(query)

    columns = [column[0] for column in cursor.description]

    print(" | ".join(columns))
    print("-" * 60)

    for row in cursor.fetchall():
        print(" | ".join(str(value) for value in row))


cursor.close()
connection.close()

print("\nAnalysis completed successfully.")