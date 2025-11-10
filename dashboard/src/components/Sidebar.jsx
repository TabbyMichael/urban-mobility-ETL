import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = ({ collapsed = false, onToggle = () => {} }) => {
  const location = useLocation();

  return (
    <div className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-top">
        <button className="toggle-btn" onClick={onToggle} aria-label="Toggle sidebar">
          {collapsed ? '➡️' : '⬅️'}
        </button>
        {!collapsed && <div className="brand">Urban Mobility</div>}
      </div>
      <nav className="sidebar-nav">
        <ul>
          <li>
            <Link 
              to="/" 
              className={location.pathname === '/' ? 'active' : ''}
            >
              <span className="icon">📊</span>
              <span className="text">Dashboard</span>
            </Link>
          </li>
          <li>
            <Link 
              to="/analytics" 
              className={location.pathname === '/analytics' ? 'active' : ''}
            >
              <span className="icon">📈</span>
              <span className="text">Analytics</span>
            </Link>
          </li>
          <li>
            <Link 
              to="/maps" 
              className={location.pathname === '/maps' ? 'active' : ''}
            >
              <span className="icon">🗺️</span>
              <span className="text">Maps</span>
            </Link>
          </li>
          <li>
            <Link 
              to="/realtime" 
              className={location.pathname === '/realtime' ? 'active' : ''}
            >
              <span className="icon">⚡</span>
              <span className="text">Real-time</span>
            </Link>
          </li>
          <li>
            <Link 
              to="/predictive" 
              className={location.pathname === '/predictive' ? 'active' : ''}
            >
              <span className="icon">🔮</span>
              <span className="text">Predictive</span>
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;