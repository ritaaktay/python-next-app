from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Document, Author
from engine import engine
from utils.green import green

# https://docs.sqlalchemy.org/en/20/orm/session_basics.html#framing-out-a-begin-commit-rollback-block
# Error handling with session.begin()
# It will try the operations, on error it will rollback() else it will commit()
with Session(engine) as session, session.begin():

    # SELECT

    query = select(Document).where(Document.title.in_(["First document", "Second document"]))

    # session.scalars returns a ScalarResult object which is iterable
    for document in session.scalars(query):
        green(document.title + " was authored by " + document.author.name)

    # Alternatively .all() can be used to get an array of the results
    green(session.scalars(query).all())

    # JOIN

    # Put forth conditions on both tables
    query = (
        select(Document)
        .join(Document.author)
        .where(Author.name == "Keith")
        .where(Document.title == "Second document")
    )

    keiths_document = session.scalars(query).one()

    green("Keith's document is: " + keiths_document.title)

    # Query for individual columns
    statement = select(Author.name)

    rows = session.execute(statement).all()

    for row in rows:
        green(row.name)

    # DATA MANIPULATION

    # Change a column value
    keiths_document.title = "Keith's document"

    green(keiths_document.title + " now has title " + keiths_document.title)

    query = select(Document).where(Document.title == "First document")

    first = session.scalars(query).one()

    # Change a relationship value
    keiths_document.author = first.author
    
    green(keiths_document.title + " now has author: " + keiths_document.author.name)
    
    # DELETE

    first = session.get(Document, 1)
    rita = session.get(Author, 1)

    # green("Rita's documents: ")
    # green(rita.documents)
    # green("Author of first document:")
    # green(first.author)

    rita.documents.remove(first)

    # When we deleted the document from Rita's documents
    # Rita was removed as the author of the document
    # So the operation works both ways

    green("Rita's documents: ")
    green(rita.documents)
    green("Author of first document:")
    green(first.author)

    session.flush()

    # The delete method will cascade to related objects
    # based on the relationship option cascade="all, delete-orphan"
    # So when we delete an Author all their Documents will be deleted

    session.delete(rita)

    # Check if the author was deleted
    query = select(Author)
    authors = session.scalars(query).all()
    green(authors)

    # Check if the document was deleted
    query = select(Document)
    documents = session.scalars(query).all()
    green(documents)

    session.commit()

