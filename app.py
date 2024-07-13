from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_caching import Cache

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configure cache
app.config['CACHE_TYPE'] = 'SimpleCache'  # Consider other options for production
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds

db = SQLAlchemy(app)
cache = Cache(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/books', methods=['GET'])
@cache.cached(timeout=60)  # Cache this route for 60 seconds
def get_books():
    books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author} for book in books]), 200

@app.route('/books/<int:id>', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # Cache varying by id
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author}), 200

@app.route('/books', methods=['POST'])
def add_books():  # Renamed to add_books to reflect bulk add
    # Invalidate cached data
    cache.delete_memoized(get_books)
    data = request.get_json()
    books_to_add = [Book(title=book_data['title'], author=book_data['author']) for book_data in data]  # Assume data is a list of books
    db.session.bulk_save_objects(books_to_add)
    db.session.commit()
    return jsonify({'message': f'{len(books_to_add)} books added successfully'}), 201

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    # Invalidate cached data
    cache.delete_memoized(get_books)
    cache.delete_memoized(get_book, id)
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.title = data['title']
    book.author = data['author']
    db.session.commit()
    return jsonify({'https://www.example.com/': 'Book updated successfully'}), 200

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    # Invalidate cached data
    cache.delete_memoized(get_books)
    cache.delete_memoized(get_book, id)
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)