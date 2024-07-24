from flask import Blueprint, request, jsonify
import logging
from your_bookknows import create_newbook, update_existing_book, fetch_book_by_id, remove_book_by_id

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

book_blueprint = Blueprint('book_blueprint', __name__)

@book_blueprint.route('/book', methods=['POST'])
def add_new_book():
    book_details = request.json
    try:
        created_book = create_new_book(book_details)
        logging.info(f"New book created with ID: {created_book['id']}")
        return jsonify(created_book), 201
    except Exception as e:  
        logging.error(f"Error creating book: {str(e)}")
        return jsonify({"error": str(e)}), 400

@book_blueprint.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = fetch_book_by_id(book_id)  
        if book:
            logging.info(f"Book fetched with ID: {book_id}")
            return jsonify(book), 200
        else:
            logging.warning(f"Book not found with ID: {book_id}")
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching book with ID {book_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@book_blueprint.route('/book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    updated_book_details = request.json
    try:
        updated_book = update_existing_book(book_id, updated_book_details)
        if updated_book:
            logging.info(f"Book updated with ID: {book_id}")
            return jsonify(updated_book), 200
        else:
            logging.warning(f"Book not found with ID: {book_id}")
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        logging.error(f"Error updating book with ID {book_id}: {str(e)}")
        return jsonify({"error": str(e)}), 400

@book_blueprint.route('/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        deletion_success = remove_book_by_id(book_id)
        if deletion_success:
            logging.info(f"Book deleted with ID: {book_id}")
            return jsonify({"message": "Book deleted successfully"}), 200
        else:
            logging.warning(f"Book not found with ID: {book_id}")
            return jsonify({"error": "Book not_found"}), 404
    except Exception as e:
        logging.error(f"Error deleting book with ID {book_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500