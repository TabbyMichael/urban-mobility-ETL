import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import io from 'socket.io-client';

// Fix for default marker icons in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const RealTime = () => {
  const [socket, setSocket] = useState(null);
  const [taxiData, setTaxiData] = useState([]);
  const [analyticsData, setAnalyticsData] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [mapLoaded, setMapLoaded] = useState(false);
  
  // Sample coordinates for NYC
  const center = [40.7128, -74.0060];

  useEffect(() => {
    // Initialize SocketIO connection
    const newSocket = io('http://localhost:5000');
    setSocket(newSocket);
    
    // Set up event listeners
    newSocket.on('connect', () => {
      setConnectionStatus('connected');
      // Start streaming when connected
      newSocket.emit('start_streaming', { dataset_id: 't29m-gskq', interval: 5 });
    });
    
    newSocket.on('disconnect', () => {
      setConnectionStatus('disconnected');
    });
    
    newSocket.on('taxi_data', (data) => {
      console.log('Received taxi data:', data);
      setTaxiData(prevData => {
        // Keep only the latest 50 data points
        const newData = [...prevData, ...data.data];
        return newData.slice(-50);
      });
    });
    
    newSocket.on('analytics_data', (data) => {
      console.log('Received analytics data:', data);
      setAnalyticsData(prevData => {
        // Keep only the latest 20 data points
        const newData = [...prevData, data.data];
        return newData.slice(-20);
      });
    });
    
    newSocket.on('error', (error) => {
      console.error('SocketIO error:', error);
    });
    
    // Ensure the map is properly loaded
    setMapLoaded(true);
    
    // Cleanup function
    return () => {
      if (newSocket) {
        newSocket.emit('stop_streaming');
        newSocket.disconnect();
      }
    };
  }, []);
  
  // Function to format large numbers
  const formatNumber = (num) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };
  
  // Function to generate random coordinates around NYC for demo
  const generateRandomCoordinates = (baseLat, baseLng, count) => {
    return Array.from({ length: count }, (_, i) => ({
      id: i,
      position: [
        baseLat + (Math.random() - 0.5) * 0.1,
        baseLng + (Math.random() - 0.5) * 0.1
      ],
      fare: Math.random() * 50 + 5,
      distance: Math.random() * 10 + 1
    }));
  };
  
  // Generate sample data for initial display
  const sampleCoordinates = generateRandomCoordinates(40.7128, -74.0060, 10);
  
  // Prepare data for charts
  const tripVolumeData = analyticsData.map((data, index) => ({
    time: new Date().toLocaleTimeString(),
    total_trips: data.total_trips || 0,
    avg_fare: data.avg_fare ? parseFloat(data.avg_fare).toFixed(2) : 0
  }));
  
  const fareDistributionData = taxiData.slice(-10).map((trip, index) => ({
    id: index,
    fare: trip.fare_amount ? parseFloat(trip.fare_amount) : 0,
    distance: trip.trip_distance ? parseFloat(trip.trip_distance) : 0
  }));

  return (
    <div>
      <h1 className="section-title">Real-time Analytics</h1>
      
      <div className="dashboard-grid">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Connection Status</h3>
          </div>
          <div className="card-value">
            <span className={`status-indicator ${connectionStatus}`}></span>
            {connectionStatus.charAt(0).toUpperCase() + connectionStatus.slice(1)}
          </div>
          <p>Real-time data streaming</p>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Active Trips</h3>
          </div>
          <div className="card-value">{taxiData.length}</div>
          <p>Currently tracked</p>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Avg. Fare</h3>
          </div>
          <div className="card-value">
            ${analyticsData.length > 0 ? 
              (analyticsData[analyticsData.length - 1].avg_fare || 0).toFixed(2) : 
              '0.00'}
          </div>
          <p>Current average</p>
        </div>
      </div>
      
      <div className="card">
        <h3 className="card-title">Live Trip Map</h3>
        <div className="maps-container" style={{ height: '500px', width: '100%' }}>
          {mapLoaded ? (
            <MapContainer 
              center={center} 
              zoom={12} 
              style={{ height: '100%', width: '100%' }}
              zoomControl={true}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              
              {taxiData.length > 0 ? (
                taxiData.slice(-20).map((trip, index) => {
                  // Generate random coordinates for demo since we don't have real pickup locations
                  const position = [
                    center[0] + (Math.random() - 0.5) * 0.1,
                    center[1] + (Math.random() - 0.5) * 0.1
                  ];
                  
                  return (
                    <Circle
                      key={index}
                      center={position}
                      radius={Math.max(100, (trip.fare_amount || 10) * 50)}
                      fillColor="#3388ff"
                      color="#3388ff"
                      fillOpacity={0.5}
                      weight={1}
                    >
                      <Popup>
                        <strong>Live Trip</strong><br />
                        Fare: ${trip.fare_amount || 'N/A'}<br />
                        Distance: {trip.trip_distance || 'N/A'} miles<br />
                        Time: {new Date().toLocaleTimeString()}
                      </Popup>
                    </Circle>
                  );
                })
              ) : (
                sampleCoordinates.map(coord => (
                  <Circle
                    key={coord.id}
                    center={coord.position}
                    radius={coord.fare * 20}
                    fillColor="#3388ff"
                    color="#3388ff"
                    fillOpacity={0.5}
                    weight={1}
                  >
                    <Popup>
                      <strong>Sample Trip</strong><br />
                      Fare: ${coord.fare.toFixed(2)}<br />
                      Distance: {coord.distance.toFixed(1)} miles
                    </Popup>
                  </Circle>
                ))
              )}
            </MapContainer>
          ) : (
            <div style={{ 
              height: '100%', 
              width: '100%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              backgroundColor: '#f0f0f0'
            }}>
              <p>Loading map...</p>
            </div>
          )}
        </div>
      </div>
      
      <div className="analytics-grid">
        <div className="card">
          <h3 className="card-title">Trip Volume Over Time</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={tripVolumeData}
                margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="time" 
                  angle={-45}
                  textAnchor="end"
                  height={60}
                  tick={{ fontSize: 12 }}
                />
                <YAxis 
                  yAxisId="trips"
                  tick={{ fontSize: 12 }}
                  tickFormatter={formatNumber}
                />
                <YAxis 
                  yAxisId="fare"
                  orientation="right"
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => `$${value}`}
                />
                <Tooltip 
                  formatter={(value, name) => {
                    if (name === 'total_trips') {
                      return [formatNumber(value), 'Trips'];
                    } else {
                      return [`$${value}`, 'Avg Fare'];
                    }
                  }}
                />
                <Legend />
                <Line 
                  yAxisId="trips"
                  type="monotone" 
                  dataKey="total_trips" 
                  name="Total Trips" 
                  stroke="#8884d8" 
                  strokeWidth={2} 
                  dot={{ r: 4 }}
                />
                <Line 
                  yAxisId="fare"
                  type="monotone" 
                  dataKey="avg_fare" 
                  name="Avg Fare" 
                  stroke="#82ca9d" 
                  strokeWidth={2} 
                  dot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="card">
          <h3 className="card-title">Fare vs Distance Distribution</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={fareDistributionData}
                margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="id" 
                  angle={-45}
                  textAnchor="end"
                  height={60}
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => `Trip ${value}`}
                />
                <YAxis 
                  yAxisId="fare"
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => `$${value}`}
                />
                <YAxis 
                  yAxisId="distance"
                  orientation="right"
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => `${value} mi`}
                />
                <Tooltip 
                  formatter={(value, name) => {
                    if (name === 'fare') {
                      return [`$${value}`, 'Fare'];
                    } else {
                      return [`${value} mi`, 'Distance'];
                    }
                  }}
                />
                <Legend />
                <Bar yAxisId="fare" dataKey="fare" name="Fare ($)" fill="#8884d8" />
                <Bar yAxisId="distance" dataKey="distance" name="Distance (mi)" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      
      <style jsx>{`
        .status-indicator {
          display: inline-block;
          width: 12px;
          height: 12px;
          border-radius: 50%;
          margin-right: 8px;
        }
        .status-indicator.connected {
          background-color: #4caf50;
        }
        .status-indicator.disconnected {
          background-color: #f44336;
        }
      `}</style>
    </div>
  );
};

export default RealTime;