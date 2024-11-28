import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  const navigationLinks = [
    { name: 'Home', path: '/' },
    { name: 'About', path: '/about' },
    { name: 'Contact', path: '/contact' },
    { name: 'Blog', path: `/blog` },
  ];

  return (
    <header>
      <nav>
        <ul>
          {navigationLinks.map((link, index) => (
            <li key={index}>
              <Link to={link.path}>{link.name}</Link>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}

export default Header;