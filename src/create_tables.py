import pyodbc


# ============================================================
# SQL Server Connection
# ============================================================

SERVER = "localhost"
DATABASE = "MovieDataWarehouse"
DRIVER = "{ODBC Driver 18 for SQL Server}"


connection_string = (
    f"DRIVER={DRIVER};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)


connection = pyodbc.connect(connection_string)

cursor = connection.cursor()


# ============================================================
# Movies Table
# ============================================================

cursor.execute("""
IF OBJECT_ID('Movies', 'U') IS NULL
BEGIN
    CREATE TABLE Movies (
        movie_id INT PRIMARY KEY,
        title NVARCHAR(255),
        original_title NVARCHAR(255),
        release_date DATE,
        original_language NVARCHAR(10),
        overview NVARCHAR(MAX),
        vote_average DECIMAL(4,2),
        vote_count INT,
        popularity DECIMAL(12,3),
        runtime INT,
        budget BIGINT,
        revenue BIGINT,
        status NVARCHAR(50),
        tagline NVARCHAR(500)
    )
END
""")


# ============================================================
# Actors Table
# ============================================================

cursor.execute("""
IF OBJECT_ID('Actors', 'U') IS NULL
BEGIN
    CREATE TABLE Actors (
        actor_id INT PRIMARY KEY,
        actor_name NVARCHAR(255)
    )
END
""")


# ============================================================
# Genres Table
# ============================================================

cursor.execute("""
IF OBJECT_ID('Genres', 'U') IS NULL
BEGIN
    CREATE TABLE Genres (
        genre_id INT PRIMARY KEY,
        genre_name NVARCHAR(100)
    )
END
""")


# ============================================================
# Movie_Actors Table
# ============================================================

cursor.execute("""
IF OBJECT_ID('Movie_Actors', 'U') IS NULL
BEGIN
    CREATE TABLE Movie_Actors (
        movie_id INT,
        actor_id INT,
        character NVARCHAR(500),
        cast_order INT,

        PRIMARY KEY (movie_id, actor_id),

        FOREIGN KEY (movie_id)
            REFERENCES Movies(movie_id),

        FOREIGN KEY (actor_id)
            REFERENCES Actors(actor_id)
    )
END
""")


# ============================================================
# Movie_Genres Table
# ============================================================

cursor.execute("""
IF OBJECT_ID('Movie_Genres', 'U') IS NULL
BEGIN
    CREATE TABLE Movie_Genres (
        movie_id INT,
        genre_id INT,

        PRIMARY KEY (movie_id, genre_id),

        FOREIGN KEY (movie_id)
            REFERENCES Movies(movie_id),

        FOREIGN KEY (genre_id)
            REFERENCES Genres(genre_id)
    )
END
""")


# ============================================================
# Commit Changes
# ============================================================

connection.commit()

print("SQL Server tables created successfully!")


# ============================================================
# Close Connection
# ============================================================

cursor.close()
connection.close()