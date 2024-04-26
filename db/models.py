from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

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
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))

    # Check how to construct the relationship - back_populates ?
    author: Mapped["Author"] = relationship(back_populates="documents")

    # Used for debugging
    def __repr__(self) -> str:
        return f"Document(id={self.id!r}, title={self.title!r}, body={self.body!r})"
    
# Author class
class Author(Base):
    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    # Check how to construct the relationship - back_populates ?
    # sqlalchemy.exc.NoForeignKeysError: Could not determine join condition 
    # between parent/child tables on relationship Document.author - there are 
    # no foreign keys linking these tables.  Ensure that referencing columns  
    # are associated with a ForeignKey or ForeignKeyConstraint, or specify a 
    # 'primaryjoin' expression.
    documents: Mapped[List["Document"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Author(id={self.id!r}, name={self.name!r})"