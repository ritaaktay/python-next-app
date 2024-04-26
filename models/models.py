from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped 
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass

class Document(Base):
    __tablename__ = 'document' 

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[str] = mapped_column(String(1000))

    # Check how to construct the relationship - back_populates ?
    author: Mapped["Author"] = relationship(back_populates="documents")

    # Used for debugging
    def __repr__(self) -> str:
        return f"Document(id={self.id!r}, title={self.title!r}, body={self.body!r})"
    

class Author(Base):
    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    # Check how to construct the relationship - back_populates ?
    documents: Mapped["Document"] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"Author(id={self.id!r}, name={self.name!r})"
    