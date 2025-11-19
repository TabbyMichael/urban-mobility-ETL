import React, { useState } from 'react';

const FullScreenChart = ({ children, title }) => {
  const [isFullScreen, setIsFullScreen] = useState(false);

  const toggleFullScreen = () => {
    setIsFullScreen(!isFullScreen);
  };

  return (
    <>
      <div style={{ position: 'relative' }}>
        {children}
        <button 
          className="fullscreen-toggle"
          onClick={toggleFullScreen}
          title="Toggle full screen"
        >
          ↗️
        </button>
      </div>
      
      {isFullScreen && (
        <div className="fullscreen-overlay" onClick={toggleFullScreen}>
          <div className="fullscreen-chart" onClick={e => e.stopPropagation()}>
            <div className="fullscreen-header">
              <h2>{title}</h2>
              <button className="close-button" onClick={toggleFullScreen}>×</button>
            </div>
            <div className="fullscreen-content">
              {children}
            </div>
          </div>
        </div>
      )}
      
      <style jsx>{`
        .fullscreen-toggle {
          position: absolute;
          top: 10px;
          right: 10px;
          background: rgba(255, 255, 255, 0.8);
          border: 1px solid #ccc;
          border-radius: 4px;
          padding: 5px 10px;
          cursor: pointer;
          z-index: 10;
          font-size: 16px;
        }
        
        .fullscreen-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.8);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 10000;
        }
        
        .fullscreen-chart {
          background: white;
          border-radius: 8px;
          width: 90%;
          height: 90%;
          display: flex;
          flex-direction: column;
        }
        
        .fullscreen-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1rem;
          border-bottom: 1px solid #eee;
        }
        
        .fullscreen-header h2 {
          margin: 0;
          font-size: 1.5rem;
        }
        
        .close-button {
          background: none;
          border: none;
          font-size: 2rem;
          cursor: pointer;
          padding: 0;
          width: 40px;
          height: 40px;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .fullscreen-content {
          flex: 1;
          padding: 1rem;
        }
        
        .fullscreen-content .chart-container {
          height: 100% !important;
        }
      `}</style>
    </>
  );
};

export default FullScreenChart;