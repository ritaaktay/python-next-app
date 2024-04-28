from sqlalchemy.orm import Session
from db.models import Author
from sqlalchemy import select
from db.engine import engine


class AuthorController:
    def get_all(self):
        with Session(engine) as session, session.begin():
            query = select(Author)
            result = session.scalars(query).all()
            authors = list(map(lambda author: author.to_dict(), result))
            return authors
    
    def add(self, data):
        with Session(engine) as session, session.begin():
            author = Author(name = data['name'])
            session.add(author)
            return author.to_dict()
        
    def update(self, data, author_id):
        with Session(engine) as session, session.begin():
            author = session.query(Author).get(author_id)
            if author is None:
                return None
            author.name = data.get('name', author.name)
            return author.to_dict()