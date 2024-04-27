from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# SQLAlchemy is an ORM (Object Relational Mapper) for SQL and Python
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html

# The docs suggest a Base class for all the models
class Base(DeclarativeBase):
    pass

# Document class
class Document(Base):
    __tablename__ = 'document' 

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[str] = mapped_column(String(1000))
    published_date: Mapped[str] = mapped_column(String(100))
    # This foreign key defines a one to many relationship 
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))

    author: Mapped["Author"] = relationship(back_populates="documents")

    # Used for debugging
    def __repr__(self) -> str:
        return f"Document(id={self.id!r}, title={self.title!r}, body={self.body!r})"
    
# Author class
class Author(Base):
    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    documents: Mapped[List["Document"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    # Used for debugging
    def __repr__(self) -> str:
        return f"Author(id={self.id!r}, name={self.name!r})"