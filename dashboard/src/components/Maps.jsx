import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, Polyline } from 'react-leaflet';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const Maps = () => {
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

  // Sample coordinates for NYC
  const center = [40.7128, -74.0060];
  
  // Sample pickup zones
  const pickupZones = [
    { id: 1, name: 'Times Square', position: [40.7580, -73.9855], trips: 1250, congestion: 85 },
    { id: 2, name: 'Penn Station', position: [40.7505, -73.9934], trips: 980, congestion: 78 },
    { id: 3, name: 'Union Square', position: [40.7359, -73.9911], trips: 870, congestion: 72 },
    { id: 4, name: 'Brooklyn Bridge', position: [40.7061, -73.9969], trips: 760, congestion: 65 },
    { id: 5, name: 'Central Park', position: [40.7812, -73.9665], trips: 650, congestion: 58 }
  ];

  // Sample route
  const sampleRoute = [
    [40.7580, -73.9855], // Times Square
    [40.7505, -73.9934], // Penn Station
    [40.7359, -73.9911], // Union Square
    [40.7061, -73.9969]  // Brooklyn Bridge
  ];

  const [mapLoaded, setMapLoaded] = useState(false);

  useEffect(() => {
    // Ensure the map is properly loaded
    setMapLoaded(true);
  }, []);

  // Mock data for additional visualizations
  const congestionData = [
    { zone: 'Times Square', level: 85, predicted: 90 },
    { zone: 'Penn Station', level: 78, predicted: 82 },
    { zone: 'Union Square', level: 72, predicted: 75 },
    { zone: 'Brooklyn Bridge', level: 65, predicted: 68 },
    { zone: 'Central Park', level: 58, predicted: 60 }
  ];

  const zoneStats = [
    { name: 'High Congestion', value: 2 },
    { name: 'Medium Congestion', value: 2 },
    { name: 'Low Congestion', value: 1 }
  ];

  const COLORS = ['#ff6b6b', '#ffd166', '#06d6a0'];
  const congestionColors = ['#ff6b6b', '#ff9e00', '#06d6a0'];

  return (
    <div>
      <h1 className="section-title">Geospatial Analytics</h1>
      
      <div className="card">
        <h3 className="card-title">Pickup Hotspots Map</h3>
        <div className="maps-container" style={{ height: '500px', width: '100%' }}>
          {mapLoaded ? (
            <MapContainer 
              center={center} 
              zoom={12} 
              style={{ height: '100%', width: '100%' }}
              zoomControl={true}
              whenCreated={(map) => {
                // Force resize to ensure proper rendering
                setTimeout(() => {
                  map.invalidateSize();
                }, 100);
              }}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              
              {/* Sample route */}
              <Polyline
                positions={sampleRoute}
                color="#3388ff"
                weight={5}
                opacity={0.7}
              />
              
              {pickupZones.map(zone => (
                <Circle
                  key={zone.id}
                  center={zone.position}
                  radius={zone.trips * 20}
                  fillColor={zone.congestion > 80 ? "#ff6b6b" : zone.congestion > 60 ? "#ff9e00" : "#06d6a0"}
                  color={zone.congestion > 80 ? "#ff6b6b" : zone.congestion > 60 ? "#ff9e00" : "#06d6a0"}
                  fillOpacity={0.5}
                  weight={1}
                >
                  <Popup>
                    <strong>{zone.name}</strong><br />
                    Trips: {formatNumber(zone.trips)}<br />
                    Congestion: {zone.congestion}%
                  </Popup>
                </Circle>
              ))}
              
              {pickupZones.map(zone => (
                <Marker key={`marker-${zone.id}`} position={zone.position}>
                  <Popup>
                    <strong>{zone.name}</strong><br />
                    Trips: {formatNumber(zone.trips)}<br />
                    Congestion: {zone.congestion}%
                  </Popup>
                </Marker>
              ))}
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
          <h3 className="card-title">Congestion Levels by Zone</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={congestionData}
                margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="zone" 
                  angle={-45}
                  textAnchor="end"
                  height={60}
                  tick={{ fontSize: 12 }}
                />
                <YAxis 
                  domain={[0, 100]} 
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => `${value}%`}
                />
                <Tooltip 
                  formatter={(value) => [`${value}%`, 'Congestion']}
                />
                <Legend />
                <Bar dataKey="level" name="Current Level (%)" fill="#ff9e00" />
                <Bar dataKey="predicted" name="Predicted Level (%)" fill="#ff6b6b" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="card">
          <h3 className="card-title">Zone Congestion Distribution</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={zoneStats}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  nameKey="name"
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                >
                  {zoneStats.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={congestionColors[index % congestionColors.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value) => [value, 'Zones']}
                />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      
      <div className="card">
        <h3 className="card-title">Real-time Traffic Flow</h3>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={[
                { time: '00:00', flow: 15 },
                { time: '04:00', flow: 10 },
                { time: '08:00', flow: 85 },
                { time: '12:00', flow: 75 },
                { time: '16:00', flow: 95 },
                { time: '20:00', flow: 65 }
              ]}
              margin={{ top: 20, right: 30, left: 20, bottom: 40 }}
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
                domain={[0, 100]} 
                tick={{ fontSize: 12 }}
                tickFormatter={(value) => `${value}%`}
              />
              <Tooltip 
                formatter={(value) => [`${value}%`, 'Traffic Flow']}
              />
              <Legend />
              <Bar dataKey="flow" name="Traffic Flow (%)" fill="#3388ff" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Maps;