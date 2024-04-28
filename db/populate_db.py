from engine import engine
from sqlalchemy.orm import Session
from models import Document, Author

# The Session object uses the engine to interact with the database
# https://docs.sqlalchemy.org/en/20/orm/session_basics.html#what-does-the-session-do
# Using with is recommended to ensure session is closed after use
with Session(engine) as session:

    # Create a new Document instance
    document1 = Document(
        title="First document", 
        body="This is the body of the first document",
        published_date="2021-01-01",
        author= Author(name="Rita")
    )

    document2 = Document(
        title="Second document", 
        body="This is the body of the second document",
        published_date="2021-01-02",
        author= Author(name="Keith")
    )

    # Add the document to the session
    session.add_all([document1, document2]) 

    # Commit the session to the database
    session.commit()