import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, AreaChart, Area } from 'recharts';
import FullScreenChart from '../components/ui/FullScreenChart';

const Dashboard = ({ data }) => {
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

  // Mock data for dashboard metrics
  const [dashboardData, setDashboardData] = useState({
    totalTrips: 1250000,
    avgFare: 18.75,
    totalRevenue: 23450000,
    avgTripDistance: 3.2,
    tripStats: [
      { hour: '00:00', trips: 1200 },
      { hour: '04:00', trips: 800 },
      { hour: '08:00', trips: 4200 },
      { hour: '12:00', trips: 3800 },
      { hour: '16:00', trips: 5200 },
      { hour: '20:00', trips: 3200 }
    ],
    paymentTypes: [
      { name: 'Credit Card', value: 65 },
      { name: 'Cash', value: 30 },
      { name: 'Digital', value: 5 }
    ],
    zonePerformance: [
      { zone: 'Manhattan', trips: 450000, revenue: 8500000 },
      { zone: 'Brooklyn', trips: 280000, revenue: 5200000 },
      { zone: 'Queens', trips: 190000, revenue: 3500000 },
      { zone: 'Bronx', trips: 150000, revenue: 2800000 },
      { zone: 'Staten Island', trips: 80000, revenue: 1500000 }
    ],
    trendData: [
      { day: 'Mon', trips: 180000, revenue: 3400000 },
      { day: 'Tue', trips: 195000, revenue: 3650000 },
      { day: 'Wed', trips: 210000, revenue: 3950000 },
      { day: 'Thu', trips: 225000, revenue: 4200000 },
      { day: 'Fri', trips: 240000, revenue: 4500000 },
      { day: 'Sat', trips: 160000, revenue: 3000000 },
      { day: 'Sun', trips: 140000, revenue: 2600000 }
    ]
  });

  // Colors for charts
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];
  const paymentColors = ['#0088FE', '#00C49F', '#FFBB28'];

  return (
    <div>
      <h1 className="section-title">Urban Mobility Dashboard</h1>
      
      {/* Key Metrics Cards */}
      <div className="dashboard-grid">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Total Trips</h3>
          </div>
          <div className="card-value">{formatNumber(dashboardData.totalTrips)}</div>
          <p>All time trips</p>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Average Fare</h3>
          </div>
          <div className="card-value">${dashboardData.avgFare}</div>
          <p>Per trip</p>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Total Revenue</h3>
          </div>
          <div className="card-value">${formatNumber(dashboardData.totalRevenue)}</div>
          <p>All time revenue</p>
        </div>
        
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Avg Trip Distance</h3>
          </div>
          <div className="card-value">{dashboardData.avgTripDistance} mi</div>
          <p>Per trip</p>
        </div>
      </div>
      
      {/* Charts Section */}
      <div className="analytics-grid">
        {/* Trip Volume by Hour */}
        <div className="card">
          <h3 className="card-title">Trip Volume by Hour</h3>
          <FullScreenChart title="Trip Volume by Hour">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart
                  data={dashboardData.tripStats}
                  margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="hour" />
                  <YAxis tickFormatter={formatNumber} />
                  <Tooltip formatter={(value) => [formatNumber(value), 'Trips']} />
                  <Area 
                    type="monotone" 
                    dataKey="trips" 
                    stroke="#8884d8" 
                    fill="#8884d8" 
                    fillOpacity={0.3} 
                    name="Trips"
                    activeDot={{ r: 6 }}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
        
        {/* Payment Types Distribution */}
        <div className="card">
          <h3 className="card-title">Payment Types</h3>
          <FullScreenChart title="Payment Types Distribution">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={dashboardData.paymentTypes}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    nameKey="name"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {dashboardData.paymentTypes.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={paymentColors[index % paymentColors.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`${value}%`, 'Percentage']} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
      </div>
      
      {/* Zone Performance */}
      <div className="card">
        <h3 className="card-title">Zone Performance</h3>
        <FullScreenChart title="Zone Performance">
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={dashboardData.zonePerformance}
                margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="zone" 
                  angle={-45}
                  textAnchor="end"
                  height={60}
                />
                <YAxis yAxisId="trips" tickFormatter={formatNumber} />
                <YAxis yAxisId="revenue" orientation="right" tickFormatter={(value) => `$${formatNumber(value)}`} />
                <Tooltip 
                  formatter={(value, name) => {
                    if (name === 'trips') {
                      return [formatNumber(value), 'Trips'];
                    } else {
                      return [`$${formatNumber(value)}`, 'Revenue'];
                    }
                  }}
                />
                <Legend />
                <Bar yAxisId="trips" dataKey="trips" name="Trips" fill="#8884d8" />
                <Bar yAxisId="revenue" dataKey="revenue" name="Revenue" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </FullScreenChart>
      </div>
      
      {/* Weekly Trend */}
      <div className="card">
        <h3 className="card-title">Weekly Trend</h3>
        <FullScreenChart title="Weekly Trend">
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={dashboardData.trendData}
                margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis yAxisId="trips" tickFormatter={formatNumber} />
                <YAxis yAxisId="revenue" orientation="right" tickFormatter={(value) => `$${formatNumber(value)}`} />
                <Tooltip 
                  formatter={(value, name) => {
                    if (name === 'trips') {
                      return [formatNumber(value), 'Trips'];
                    } else {
                      return [`$${formatNumber(value)}`, 'Revenue'];
                    }
                  }}
                />
                <Legend />
                <Line 
                  yAxisId="trips" 
                  type="monotone" 
                  dataKey="trips" 
                  name="Trips" 
                  stroke="#8884d8" 
                  strokeWidth={2} 
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }}
                />
                <Line 
                  yAxisId="revenue" 
                  type="monotone" 
                  dataKey="revenue" 
                  name="Revenue" 
                  stroke="#82ca9d" 
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
  );
};

export default Dashboard;