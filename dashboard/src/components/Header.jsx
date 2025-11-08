import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-content">
        <h1>Urban Mobility Analytics</h1>
        <nav>
          <ul>
            <li><a href="/">Dashboard</a></li>
            <li><a href="/analytics">Analytics</a></li>
            <li><a href="/maps">Maps</a></li>
            <li><a href="/predictive">Predictive</a></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;