import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ScatterChart, Scatter } from 'recharts';
import FullScreenChart from '../components/ui/FullScreenChart';

const Analytics = ({ data }) => {
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

  // Mock data for analytics
  const [analyticsData, setAnalyticsData] = useState({
    tripDistribution: [
      { day: 'Monday', yellow: 4000, green: 2500, uber: 3500 },
      { day: 'Tuesday', yellow: 4200, green: 2600, uber: 3700 },
      { day: 'Wednesday', yellow: 4500, green: 2800, uber: 4000 },
      { day: 'Thursday', yellow: 4700, green: 3000, uber: 4200 },
      { day: 'Friday', yellow: 5000, green: 3200, uber: 4500 },
      { day: 'Saturday', yellow: 3500, green: 2200, uber: 3000 },
      { day: 'Sunday', yellow: 3000, green: 2000, uber: 2500 }
    ],
    fareAnalysis: [
      { range: '< $10', count: 15000 },
      { range: '$10-20', count: 35000 },
      { range: '$20-30', count: 25000 },
      { range: '$30-50', count: 18000 },
      { range: '> $50', count: 7000 }
    ],
    speedAnalysis: [
      { hour: '00:00', speed: 15.2 },
      { hour: '04:00', speed: 18.5 },
      { hour: '08:00', speed: 8.7 },
      { hour: '12:00', speed: 12.3 },
      { hour: '16:00', speed: 9.8 },
      { hour: '20:00', speed: 14.1 }
    ],
    passengerDemand: [
      { location: 'Times Square', demand: 95 },
      { location: 'Penn Station', demand: 88 },
      { location: 'Union Square', demand: 82 },
      { location: 'Brooklyn Bridge', demand: 75 },
      { location: 'Central Park', demand: 70 },
      { location: 'Wall Street', demand: 85 },
      { location: 'LaGuardia', demand: 65 },
      { location: 'JFK Airport', demand: 60 }
    ],
    tripDuration: [
      { duration: '< 5 min', percentage: 15 },
      { duration: '5-15 min', percentage: 45 },
      { duration: '15-30 min', percentage: 25 },
      { duration: '30-60 min', percentage: 10 },
      { duration: '> 60 min', percentage: 5 }
    ],
    correlationData: [
      { temp: 32, trips: 2800 },
      { temp: 45, trips: 3200 },
      { temp: 55, trips: 3800 },
      { temp: 65, trips: 4500 },
      { temp: 75, trips: 5200 },
      { temp: 85, trips: 4800 },
      { temp: 95, trips: 4200 }
    ]
  });

  // Colors for charts
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];
  const fareColors = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

  return (
    <div>
      <h1 className="section-title">Advanced Analytics</h1>
      
      {/* Trip Distribution */}
      <div className="card">
        <h3 className="card-title">Trip Distribution by Day and Service</h3>
        <FullScreenChart title="Trip Distribution by Day and Service">
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={analyticsData.tripDistribution}
                margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="day" 
                  angle={-45}
                  textAnchor="end"
                  height={60}
                />
                <YAxis tickFormatter={formatNumber} />
                <Tooltip formatter={(value) => [formatNumber(value), 'Trips']} />
                <Legend />
                <Bar dataKey="yellow" name="Yellow Taxi" fill="#FFD700" />
                <Bar dataKey="green" name="Green Taxi" fill="#32CD32" />
                <Bar dataKey="uber" name="Uber" fill="#000000" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </FullScreenChart>
      </div>
      
      <div className="analytics-grid">
        {/* Fare Analysis */}
        <div className="card">
          <h3 className="card-title">Fare Distribution</h3>
          <FullScreenChart title="Fare Distribution">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={analyticsData.fareAnalysis}
                    cx="50%"
                    cy="50%"
                    labelLine={true}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="count"
                    nameKey="range"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    activeIndex={0}
                  >
                    {analyticsData.fareAnalysis.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={fareColors[index % fareColors.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [formatNumber(value), 'Trips']} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
        
        {/* Speed Analysis */}
        <div className="card">
          <h3 className="card-title">Average Speed by Hour</h3>
          <FullScreenChart title="Average Speed by Hour">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={analyticsData.speedAnalysis}
                  margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="hour" />
                  <YAxis domain={[0, 20]} tickFormatter={(value) => `${value} mph`} />
                  <Tooltip formatter={(value) => [`${value} mph`, 'Speed']} />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="speed" 
                    name="Average Speed" 
                    stroke="#8884d8" 
                    strokeWidth={2}
                    dot={{ r: 4 }}
                    activeDot={{ r: 6 }} 
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
      </div>
      
      {/* Passenger Demand Heatmap */}
      <div className="card">
        <h3 className="card-title">Passenger Demand by Location</h3>
        <FullScreenChart title="Passenger Demand by Location">
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={analyticsData.passengerDemand}>
                <PolarGrid />
                <PolarAngleAxis dataKey="location" />
                <PolarRadiusAxis angle={30} domain={[0, 100]} />
                <Radar
                  name="Demand"
                  dataKey="demand"
                  stroke="#8884d8"
                  fill="#8884d8"
                  fillOpacity={0.6}
                  activeDot={{ r: 6 }}
                />
                <Tooltip formatter={(value) => [`${value}%`, 'Demand']} />
                <Legend />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </FullScreenChart>
      </div>
      
      <div className="analytics-grid">
        {/* Trip Duration */}
        <div className="card">
          <h3 className="card-title">Trip Duration Distribution</h3>
          <FullScreenChart title="Trip Duration Distribution">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={analyticsData.tripDuration}
                  layout="vertical"
                  margin={{ top: 20, right: 30, left: 60, bottom: 20 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" domain={[0, 50]} tickFormatter={(value) => `${value}%`} />
                  <YAxis 
                    dataKey="duration" 
                    type="category" 
                    width={80}
                  />
                  <Tooltip formatter={(value) => [`${value}%`, 'Percentage']} />
                  <Legend />
                  <Bar 
                    dataKey="percentage" 
                    name="Percentage" 
                    fill="#82ca9d" 
                    barSize={30}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
        
        {/* Weather Correlation */}
        <div className="card">
          <h3 className="card-title">Temperature vs Trip Volume</h3>
          <FullScreenChart title="Temperature vs Trip Volume">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart
                  margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
                >
                  <CartesianGrid />
                  <XAxis 
                    type="number" 
                    dataKey="temp" 
                    name="Temperature" 
                    unit="°F" 
                  />
                  <YAxis 
                    type="number" 
                    dataKey="trips" 
                    name="Trips" 
                    tickFormatter={formatNumber}
                  />
                  <Tooltip 
                    cursor={{ strokeDasharray: '3 3' }}
                    formatter={(value, name) => {
                      if (name === 'temp') {
                        return [`${value}°F`, 'Temperature'];
                      } else {
                        return [formatNumber(value), 'Trips'];
                      }
                    }}
                  />
                  <Legend />
                  <Scatter 
                    name="Trip Volume" 
                    data={analyticsData.correlationData} 
                    fill="#8884d8" 
                    activeDot={{ r: 8 }}
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
      </div>
    </div>
  );
};

export default Analytics;