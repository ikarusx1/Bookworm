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

if __name__ == "__main__":
    session = Session()
    new_book = Book(title="Example Title", author="Example Author", genre="Fiction", review=4.5)
    session.add(new_book)
    session.commit()

    books = session.query(Book).all()
    for book in books:
        print(f"{book.title}, {book.author}, {book.genre}, {book.review}")

    session.close()