from flask import Blueprint, request
from your_book_controller import create_book, update_book, get_book, delete_book

books_bp = Blueprint('books_bp', __name__)

@books_bp.route('/book', methods=['POST'])
def add_book():
    data = request.json
    return create_book(data)

@books_bp.route('/book/<int:book_id>', methods=['GET'])
def retrieve_book(book_id):
    return get(book_id)

@books_bp.route('/book/<int:book_id>', methods=['PUT'])
def change_book(book_id):
    data = request.json
    return update_book(book_id, data)

@books_bp.route('/book/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    return delete_book(book_id)