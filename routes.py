from flask import Blueprint, request, jsonify
from your_book_controller import create_book, update_book, get_book, delete_book

books_bp = Blueprint('books_bp', __name__)

@booksa_bp.route('/book', methods=['POST'])
def add_book():
    data = request.json
    try:
        book = create_book(data)
        return jsonify(book), 201  # Assuming create_book returns the created book dict/json
    except Exception as e:  # Consider using more specific exception handling based on your application's logic
        return jsonify({"error": str(e)}), 400

@books_bp.route('/book/<int:book_id>', methods=['GET'])
def retrieve_book(book_id):
    try:
        book = get_book(book_id)  # Make sure get_book is correctly referenced here, previously it was just get().
        if book:
            return jsonify(book), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@books_bp.route('/book/<int:book_id>', methods=['PUT'])
def change_book(book_id):
    data = request.json
    try:
        book = update_book(book_id, data)
        if book:
            return jsonify(book), 200  # Assuming update_book returns the updated book dict/json
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@books_bp.route('/book/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    try:
        result = delete_book(book_id)
        if result:
            return jsonify({"message": "Book deleted successfully"}), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500