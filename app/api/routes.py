from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema , books_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'naw'}

@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    isbn = request.json['isbn']
    title = request.json['title']
    author = request.json['author']
    length = request.json['length']
    genre = request.json['genre']
    year = request.json['year']
    user_token = current_user_token.token  

    book = Book(isbn, title, author, length, genre, year, user_token)
    
    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required
def get_book(current_user_token):
    a_user = current_user_token.token 
    books = Book.query.filter_by(user_token = a_user).all()
    response = book_schema.dump(books)
    return jsonify(response)

@api.route('/books/<isbn>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, isbn):
    book = Book.query.get(isbn)
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/<isbn>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token ,isbn):
    book = Book.query.get(isbn)
    book.title = request.json['title']
    book.author = request.json['author']
    book.length = request.json['length']
    book.genre = request.json['genre']
    book.year = request.json['year']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)


@api.route('/books/<isbn>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, isbn):
    book = Book.query.get(isbn)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)