from models import Base
from engine import engine
from models import Author

# Delete existing tables

Base.metadata.drop_all(engine)

# Create the tables of all Base subclasses

# The usual way to issue CREATE is to use create_all() on the MetaData object. 
# This method will issue queries that first check for the existence of each 
# individual table, and if not found will issue the CREATE statements
# https://docs.sqlalchemy.org/en/20/core/metadata.html 

Base.metadata.create_all(engine)
