import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import Analytics from './components/Analytics';
import Maps from './components/Maps';
import Predictive from './components/Predictive';
import RealTime from './components/RealTime';
import Header from './components/Header';
import './App.css';
import './components/AppLayout.css';

function App() {
  const [isBackendHealthy, setIsBackendHealthy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  useEffect(() => {
    // Check backend health
    const checkBackendHealth = async () => {
      try {
        const response = await fetch('/api/v1/health');
        setIsBackendHealthy(response.ok);
      } catch (error) {
        console.error('Backend health check failed:', error);
        setIsBackendHealthy(false);
      } finally {
        setLoading(false);
      }
    };

    checkBackendHealth();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!isBackendHealthy) {
    return (
      <div className="error-container">
        <h1>Backend Connection Error</h1>
        <p>Unable to connect to the backend API. Please ensure the server is running.</p>
        <button onClick={() => window.location.reload()}>Retry</button>
      </div>
    );
  }

  return (
    <Router>
      <div className="app">
        <div className="main-container">
          <Sidebar 
            sidebarCollapsed={sidebarCollapsed} 
            setSidebarCollapsed={setSidebarCollapsed} 
          />
          <div className={`content ${sidebarCollapsed ? 'collapsed' : ''}`}>
            <Header 
              sidebarCollapsed={sidebarCollapsed} 
              setSidebarCollapsed={setSidebarCollapsed} 
            />
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/maps" element={<Maps />} />
              <Route path="/predictive" element={<Predictive />} />
              <Route path="/realtime" element={<RealTime />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;