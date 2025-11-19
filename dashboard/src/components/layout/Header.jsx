import React from 'react';
import './Header.css';

const Header = ({ sidebarCollapsed, setSidebarCollapsed }) => {
  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  return (
    <header className="header">
      <div className="header-content">
        <button className="menu-toggle" onClick={toggleSidebar}>
          {sidebarCollapsed ? '☰' : '✕'}
        </button>
        <h1>Urban Mobility & Transportation Analytics</h1>
      </div>
    </header>
  );
};

export default Header;