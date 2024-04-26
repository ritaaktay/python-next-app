from sqlalchemy.orm import Session 
from create_db import engine
from models import Document, Author

# The Session object uses the engine to interact with the database
# Using with is recommended to ensure session is closed after use
with Session(engine) as session:

    # Create a new Document instance
    document = Document(
        title="First document", 
        body="This is the body of the first document",
        author=Author(name="Rita")
    )

    # Add the document to the session
    session.add_all([document]) 

    # Commit the session to the database
    session.commit()