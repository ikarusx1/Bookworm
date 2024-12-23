import React, { useState, useEffect } from 'react';

const BookForm = ({ onSubmitBook, initialValues }) => {
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    genre: '',
    review: '',
  });

  useEffect(() => {
    if (initialValues) {
      setFormData({
        title: initialValues.title || '',
        author: initialValues.author || '',
        genre: initialValues.genre || '',
        review: initialValues.review || '',
      });
    }
  }, [initialValues]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!formData.title || !formData.author) {
      alert('Title and Author are required!');
      return;
    }
    onSubmitBook(formData);
    setFormData({
      title: '',
      author: '',
      genre: '',
      review: '',
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Title:</label>
        <input
          type="text"
          name="title"
          value={formData.title}
          onChange={handleChange}
        />
      </div>
      <div>
        <label>Author:</label>
        <input
          type="text"
          name="author"
          value={formData.author}
          onChange={handleChange}
        />
      </div>
      <div>
        <label>Genre:</label>
        <select name="genre" value={formData.genre} onChange={handleChange}>
          <option value="">Select genre</option>
          <option value="Fiction">Fiction</option>
          <option value="Non-Fiction">Non-Fiction</option>
          <option value="Fantasy">Fantasy</option>
          <option value="Mystery">Mystery</option>
        </select>
      </div>
      <div>
        <label>Review:</label>
        <textarea
          name="review"
          value={formData.review}
          onChange={handleChange}
        />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default BookForm;