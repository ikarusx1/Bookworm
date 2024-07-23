from flask import Blueprint, request, jsonify
from your_book_controller import create_new_book, update_existing_book, fetch_book_by_id, remove_book_by_id

book_blueprint = Blueprint('book_blueprint', __name__)

@book_blueprint.route('/book', methods=['POST'])
def add_new_book():
    book_details = request.json
    try:
        created_book = create_new_book(book_details)
        return jsonify(created_book), 201
    except Exception as e:  
        return jsonify({"error": str(e)}), 400

@book_blueprint.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = fetch_book_by_id(book_id)  
        if book:
            return jsonify(book), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@book_blueprint.route('/book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    updated_book_details = request.json
    try:
        updated_book = update_existing_book(book_id, updated_book_details)
        if updated_book:
            return jsonify(updated_book), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@book_blueprint.route('/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        deletion_success = remove_book_by_id(book_id)
        if deletion_success:
            return jsonify({"message": "Book deleted successfully"}), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"deste": str(e)}), 500