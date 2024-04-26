# Create an in-memory SQLite database
from sqlalchemy import create_engine
from models import Base

engine = create_engine('sqlite://', echo=True)

# Create the tables of all Base subclasses
Base.metadata.create_all(engine)