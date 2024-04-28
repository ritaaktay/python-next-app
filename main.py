# https://fastapi.tiangolo.com/
# FastAPI is a modern, fast (high-performance), web framework for 
# building APIs with Python 3.8+.

# Docs / Tutorial
# https://fastapi.tiangolo.com/tutorial/

from typing import Union
from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.engine import engine
from db.utils.green import green
from db.models import Document, Author
from schemas import ( 
    AuthorBase, AuthorUpdate, AuthorResponse, Error,
    DocumentBase, DocumentUpdate, DocumentResponse 
)
from controllers.document_controller import document_controller
from controllers.author_controller import author_controller

app = FastAPI()

# FastAPI will recognize that the function parameters that match path parameters
# should be taken from the path, and that function parameters that are declared 
# to be Pydantic models should be taken from the request body.

@app.get("/documents")
def get_all_documents() -> list[DocumentBase] | Error:
    with Session(engine) as session, session.begin():
        try:
            return document_controller.get_all()
        except Exception as e:
            return handle_exception(e)

@app.get("/documents/{document_id}")
def get_document_by_id(document_id) -> DocumentResponse | Error:
    try: 
        document = document_controller.get_by_id(document_id)
        if document is None:
            return not_found()
        return document
    except Exception as e:
        handle_exception(e)
            
# Add a document
@app.post("/documents")
def add_document(document: DocumentBase) -> DocumentBase | Error:
    try:
        return document_controller.add(document.model_dump())
    except Exception as e:
        return handle_exception(e)

# Update a document
@app.put("/documents/{document_id}", response_model= DocumentBase | Error)
def update_document(document_id, document: DocumentUpdate):
    try:
        document = document_controller.update(document.model_dump(), document_id)
        if document is None:
            return not_found()
        return document
    except Exception as e:
        return handle_exception(e)

# 404 Not found
def not_found():
    return { "error": "Not found"}

# Exceptions
def handle_exception(e):
    return {"error": repr(e)}