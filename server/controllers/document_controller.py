from sqlalchemy.orm import Session
from db.models import Document, Author
from sqlalchemy import select
from db.engine import engine


class DocumentController:
    def get_all(self):
        with Session(engine) as session, session.begin():
                query = select(Document)
                result = session.scalars(query).all()
                documents= list(map(lambda document: document.to_dict(), result))
                return documents
    
    def get_all_by_author(self, author_id):
        with Session(engine) as session, session.begin():
            query = select(Document).where(Document.author_id == author_id)
            result = session.scalars(query).all()
            documents = list(map(lambda document: document.to_dict(), result))
            return documents
        
    def get_by_id(self, document_id):
        with Session(engine) as session, session.begin():
            document = session.query(Document).get(document_id)
            if document is None:
                return None
            return document.to_dict()
        
    def add(self, data):
        with Session(engine) as session, session.begin():
            document = Document(
                title=data["title"], 
                body=data["body"],
                published_date=data["published_date"],
                author = Author(name = data["author"]["name"])
            )
            session.add(document)
            return document.to_dict()
        
    def update(self, data, document_id):
        with Session(engine) as session, session.begin():
            document = session.query(Document).get(document_id)
            if document is None:
                return None
            document.title = data.get('title', document.title)
            document.body = data.get('body', document.body)
            document.published_date = data.get('published_date', document.published_date)
            # If author exists, point document to existing author
            # If not, create new author, point document to new author
            if data.get('author') is not None:
                name = data.get('author').get('name')   
                query = select(Author).where(Author.name == name)
                response = session.scalars(query).first()
                if response:
                    document.author_id = response.id
                else:
                    author = Author(name = name)
                    session.add(author)
                    session.flush()
                    document.author_id = author.id
            return document.to_dict()
        
document_controller = DocumentController()