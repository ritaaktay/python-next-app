from flask import Flask, jsonify, make_response, send_file, request
from db.engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import Document, Author
from db.utils.green import green

# https://flask.palletsprojects.com/en/3.0.x/
app = Flask(__name__)

# This function takes a greeting from the url path
# And a name from the query string to greet user
@app.route('/greet/<greeting>', methods=['GET'])
def greet(greeting):
    # Get /hello?key=value&name=Rita
    # query = {"key": "value", "name": "Rita"} 
    query = request.args 
    res = make_response("%s %s" %(greeting, query.get('name')))
    res.headers['Content-type'] = 'text'
    return res

# This function returns the profile image from server
@app.route('/profile', methods=['GET'])
def profile():
    return send_file('public/profile.jpg')


# Return all documents
@app.route('/documents', methods=['GET'])
def get_all_documents(): 
    with Session(engine) as session, session.begin():
        try:
            query = select(Document)
            result = session.scalars(query).all()
            documents= list(map(lambda document: document.to_dict(), result))
            # Turns JSON output into a Response object with the application/json mimetype
            return jsonify(documents)
        except Exception as e:
            return handle_exception(e)
       
# Return all documents of a given author
@app.route('/documents/<author_id>', methods=['GET'])
def get_all_documents_by_author(author_id): 
    with Session(engine) as session, session.begin():
        try:
            query = select(Document).where(Document.author_id == author_id)
            result = session.scalars(query).all()
            documents = list(map(lambda document: document.to_dict(), result))
            return jsonify(documents)
        except Exception as e:
            return handle_exception(e)

# Add a document 
@app.route('/documents', methods=['POST'])
def add_document():
    with Session(engine) as session, session.begin():
        try:
            data = request.json
            document = Document(
                title=data['title'], 
                body=data['body'],
                published_date=data['published_date'],
                author = Author(name = data['author']['name'])
            )
            session.add(document)
            return jsonify(document.to_dict())
        except Exception as e:
            return handle_exception(e)

# Update a document
@app.route('/documents/<document_id>', methods=['PUT'])
def update_document(document_id):
    with Session(engine) as session, session.begin():
        try:
            data = request.json 
            document = session.query(Document).get(document_id)
            if document is None:
                return not_found()
            document.title = data.get('title', document.title)
            document.body = data.get('body', document.body)
            document.published_date = data.get('published_date', document.published_date)
            # If author exists, point document to existing author
            # If not, create new author, point document to new author
            if data["author"]:
                query = select(Author).where(Author.name == data['author']['name'])
                response = session.scalars(query).first()
                if response:
                    document.author_id = response.id
                else:
                    author = Author(name = data['author']['name'])
                    session.add(author)
                    session.flush()
                    document.author_id = author.id
            return jsonify(document.to_dict())
        except Exception as e:
            return handle_exception(e)

# Get all authors
@app.route('/authors', methods=['GET'])
def get_all_authors():
    with Session(engine) as session, session.begin():
        try:
            query = select(Author)
            result = session.scalars(query).all()
            authors = list(map(lambda author: author.to_dict(), result))
            return jsonify(authors)
        except Exception as e:
            return handle_exception(e)

# Add an author
@app.route('/authors', methods=['POST'])
def add_author():
    with Session(engine) as session, session.begin():
        try:
            data = request.json
            author = Author(name = data['name'])
            session.add(author)
            return jsonify(author.to_dict())
        except Exception as e:
           return handle_exception()

# Update an author
@app.route('/authors/<author_id>', methods=['PUT'])
def update_author(author_id):
    with Session(engine) as session, session.begin():
        try:
            data = request.json
            author = session.query(Author).get(author_id)
            if author is None:
                return not_found()
            author.name = data.get('name', author.name)
            return jsonify(author.to_dict())
        except Exception as e:
            return handle_exception()

# 404 Not found
def not_found():
    res = jsonify({ "error": "Not found"})
    res.status_code = 404
    return res

# Exceptions
def handle_exception(e):
    res = jsonify({"error": repr(e)})
    res.status_code = 500
    return res