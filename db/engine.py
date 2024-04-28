from sqlalchemy import URL, create_engine

# Create an in-memory SQLite database
# engine = create_engine('sqlite://', echo=True)

# More on engines
# https://docs.sqlalchemy.org/en/20/core/engines.html 

url = URL.create(
    "postgresql+psycopg2",
    username="postgres",
    password="73627362",
    host="localhost",
    database="cpr_test",
)


# Connect to PostgreSQL database
try:
    engine = create_engine(url)
except Exception as e:
    print('Unable to access postgresql database', repr(e))