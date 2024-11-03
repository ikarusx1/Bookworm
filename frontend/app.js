const BASE_URL = 'http://your-api-url.com/api/books';

async function fetchBooks(filterText = '') {
  try {
    const response = await fetch(`${BASE_URL}?filter=${filterText}`);
    if (!response.ok) throw new Error('Failed to fetch books');
    const books = await response.json();
    displayBooks(books);
  } catch (error) {
    console.error('Error fetching books:', error);
  }
}

function displayBooks(books) {
  const booksContainer = document.getElementById('booksContainer');
  const sortType = document.getElementById('sortBooks').value;
  booksContainer.innerHTML = '';

  if(sortType !== 'none') {
    books.sort((a,b) => {
      if(sortType === 'title') {
        return a.title.localeCompare(b.title);
      } else if(sortType === 'author') {
        return a.author.localeCompare(b.author);
      }
    });
  }

  books.forEach(book => {
    const bookElement = document.createElement('div');
    bookElement.innerHTML = `
      <h3>${book.title}</h3>
      <p>${book.author}</p>
      <button onclick="deleteBook('${book.id}')">Delete</button>
      <button onclick="editBook('${book.id}')">Edit</button>
    `;
    booksContainer.appendChild(bookElement);
  });
}

async function createBook(bookData) {
  try {
    const response = await fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bookData),
    });
    if (!response.ok) throw new Error('Failed to create book');
    fetchBooks();
  } catch (error) {
    console.error('Error creating book:', error);
  }
}

async function deleteBook(bookId) {
  try {
    const response = await fetch(`${BASE_URL}/${bookId}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete book');
    fetchBooks();
  } catch (error) {
    console.error('Error deleting book:', error);
  }
}

async function updateBook(bookId, newBookData) {
  try {
    const response = await fetch(`${BASE_URL}/${bookId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newBookData),
    });
    if (!response.ok) throw new Error('Failed to update book');
    fetchBooks();
  } catch (error) {
    console.error('Error updating book:', error);
  }
}

document.getElementById('createBookForm').addEventListener('submit', event => {
  event.preventDefault();
  const bookData = {
    title: event.target.title.value,
    author: event.target.author.value,
  };
  createBook(bookData);
});

document.getElementById('filterBooks').addEventListener('input', event => {
  const filterText = event.target.value;
  fetchBooks(filterText);
});

document.getElementById('sortBooks').addEventListener('change', () => {
  fetchBooks(document.getElementById('filterBooks').value);
});

document.addEventListener('DOMContentLoaded', () => {
  fetchBooks();
});