const BASE_URL = 'http://your-api-url.com/api/books';

async function fetchBooks(filterText = '') {
  try {
    const response = await fetch(`${BASE_URL}?filter=${encodeURIComponent(filterText)}`);
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

  const sorter = {
    'title': (a, b) => a.title.localeCompare(b.title),
    'author': (a, b) => a.author.localeCompare(b.author)
  };

  if(sortType !== 'none' && sorter[sortType]) {
    books.sort(sorter[sortType]);
  }

  books.forEach(book => {
    const bookElement = document.createElement('div');
    bookElement.innerHTML = `
      <h3>${book.title}</h3>
      <p>${book.author}</p>
      <button onclick="deleteBook('${book.id}')">Delete</button>
      <button onclick="editBook('${book.id}', '${book.title}', '${book.author}')">Edit</button>
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
    await fetchBooks();
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
    await fetchBooks();
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
    await fetchBooks();
  } catch (error) {
    console.error('Error updating book:', error);
  }
}

document.getElementById('createBookForm').addEventListener('submit', event => {
  event.preventDefault();
  const formData = new FormData(event.target);
  const bookData = {
    title: formData.get('title'),
    author: formData.get('author'),
  };
  createBook(bookData);
});

document.getElementById('filterBooks').addEventListener('input', debounceEvent(() => {
  fetchBooks(document.getElementById('filterBooks').value);
}, 250));

document.getElementById('sortBooks').addEventListener('change', () => {
  fetchBooks(document.getElementById('filterBooks').value);
});

document.addEventListener('DOMContentLoaded', () => {
  fetchBooks();
});

function debounceEvent(callback, delay = 1000) {
  let timerId;
  return (...args) => {
    clearTimeout(timerId);
    timerId = setTimeout(() => {
      callback.apply(this, args);
    }, delay);
  };
}