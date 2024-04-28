from flask import Flask, jsonify, make_response, send_file, request
from db.engine import engine
from sqlalchemy.orm import Session
from db.models import Document, Author
from sqlalchemy import select
from db.utils.green import green
from controllers.document_controller import DocumentController
from controllers.author_controller import AuthorController

# https://flask.palletsprojects.com/en/3.0.x/
app = Flask(__name__)

document_controller = DocumentController()
author_controller = AuthorController()

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
            documents = document_controller.get_all()
            return jsonify(documents)
        except Exception as e:
            return handle_exception(e)

@app.route('/documents/<author_id>', methods=['GET'])
def get_all_documents_by_author(author_id): 
        try:
           return jsonify(document_controller.get_all_by_author(author_id))
        except Exception as e:
            return handle_exception(e)

# Add a document 
@app.route('/documents', methods=['POST'])
def add_document():
        try:
            document = document_controller.add(request.json)
            return jsonify(document)
        except Exception as e:
            return handle_exception(e)

# Update a document
@app.route('/documents/<document_id>', methods=['PUT'])
def update_document(document_id):
    try:
        return jsonify(document_controller.update(request.json, document_id))
    except Exception as e:
        return handle_exception(e)

# Get all authors
@app.route('/authors', methods=['GET'])
def get_all_authors():
        try:
            return jsonify(author_controller.get_all())
        except Exception as e:
            return handle_exception(e)

# Add an author
@app.route('/authors', methods=['POST'])
def add_author():
    with Session(engine) as session, session.begin():
        try:
            return jsonify(author_controller.add(request.json))
        except Exception as e:
            return handle_exception(e)

# Update an author
@app.route('/authors/<author_id>', methods=['PUT'])
def update_author(author_id):
    try:
        author = author_controller.update(request.json, author_id)
        if author is None:
            return not_found()
        return jsonify(author)
    except Exception as e:
        return handle_exception(e)

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