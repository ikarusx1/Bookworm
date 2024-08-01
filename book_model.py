import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String)
    review = Column(Float)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///books.db")

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def add_books_in_batch(session, books_data):
    """
    Adds multiple Book records to the database in a single transaction.

    :param session: The session object for database interaction
    :param books_data: A list of dictionaries, where each dictionary represents a book's data
    """
    books = [Book(**data) for data in books_data]
    session.add_all(books)
    session.commit()

if __name__ == "__main__":
    session = Session()
    
    books_data = [
        {"title": "Example Title 1", "author": "Example Author 1", "genre": "Fiction", "review": 4.5},
        {"title": "Example Title 2", "author": "Example Author 2", "genre": "Non-Fiction", "review": 4.2}
    ]

    add_books_in_batch(session, books_data)

    # Fetch and print all books in the database
    books = session.query(Book).all()
    for book in books:
        print(f"{book.title}, {book.author}, {book.genre}, {book.review}")

    session.close()