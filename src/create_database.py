import pyodbc


SERVER = "localhost"
DATABASE = "master"
DRIVER = "{ODBC Driver 18 for SQL Server}"


connection_string = (
    f"DRIVER={DRIVER};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)


connection = pyodbc.connect(connection_string)

# CREATE DATABASE must run outside a transaction
connection.autocommit = True

cursor = connection.cursor()


database_name = "MovieDataWarehouse"


cursor.execute(f"""
IF DB_ID('{database_name}') IS NULL
BEGIN
    CREATE DATABASE {database_name}
END
""")


print(f"Database '{database_name}' is ready.")


cursor.close()
connection.close()