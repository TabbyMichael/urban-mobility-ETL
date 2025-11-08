import React from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <nav>
        <ul>
          <li>
            <Link to="/" className="nav-link">
              <span className="nav-icon">📊</span>
              Dashboard
            </Link>
          </li>
          <li>
            <Link to="/analytics" className="nav-link">
              <span className="nav-icon">📈</span>
              Analytics
            </Link>
          </li>
          <li>
            <Link to="/maps" className="nav-link">
              <span className="nav-icon">🗺️</span>
              Maps
            </Link>
          </li>
          <li>
            <Link to="/predictive" className="nav-link">
              <span className="nav-icon">🔮</span>
              Predictive
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;