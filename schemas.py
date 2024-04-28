from pydantic import BaseModel

# More on how to use pydantic BaseModels with SQLAlchemy models
# https://fastapi.tiangolo.com/tutorial/sql-databases/
class AuthorBase(BaseModel):
    name: str

class AuthorResponse(AuthorBase):
    id: int

class AuthorUpdate(AuthorBase):
    name: str | None = None

class DocumentBase(BaseModel):
    title: str
    body: str 
    published_date: str
    author: AuthorBase

class DocumentResponse(DocumentBase):
    id: int
    author_id: int

class DocumentUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    published_date: str | None = None
    author: AuthorBase | None = None

class Error(BaseModel):
    error: str