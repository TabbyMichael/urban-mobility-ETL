import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area, PieChart, Pie, Cell, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ScatterChart, Scatter } from 'recharts';
import FullScreenChart from '../components/ui/FullScreenChart';

const Predictive = ({ data }) => {
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

  // Mock data for predictive models
  const [predictiveData, setPredictiveData] = useState({
    demandForecast: [
      { time: '00:00', actual: 120, predicted: 115, lower: 100, upper: 130 },
      { time: '04:00', actual: 80, predicted: 85, lower: 70, upper: 100 },
      { time: '08:00', actual: 420, predicted: 410, lower: 380, upper: 440 },
      { time: '12:00', actual: 380, predicted: 390, lower: 360, upper: 420 },
      { time: '16:00', actual: 520, predicted: 530, lower: 500, upper: 560 },
      { time: '20:00', actual: 320, predicted: 310, lower: 280, upper: 340 }
    ],
    fraudDetection: [
      { type: 'Normal', count: 950 },
      { type: 'Suspicious', count: 50 }
    ],
    congestion: [
      { route: 'Route 1', level: 75, predicted: 80 },
      { route: 'Route 2', level: 60, predicted: 65 },
      { route: 'Route 3', level: 45, predicted: 50 },
      { route: 'Route 4', level: 30, predicted: 35 },
      { route: 'Route 5', level: 15, predicted: 20 }
    ],
    modelPerformance: [
      { model: 'Trip Demand', accuracy: 87, rmse: 12.5 },
      { model: 'Fraud Detection', accuracy: 92, rmse: 8.3 },
      { model: 'Congestion', accuracy: 78, rmse: 15.2 },
      { model: 'Route Optimization', accuracy: 85, rmse: 10.7 }
    ],
    routeOptimization: [
      { route: 'A→B', current_time: 25, optimized_time: 20, savings: 5 },
      { route: 'C→D', current_time: 40, optimized_time: 32, savings: 8 },
      { route: 'E→F', current_time: 18, optimized_time: 15, savings: 3 },
      { route: 'G→H', current_time: 35, optimized_time: 28, savings: 7 }
    ],
    anomalyDetection: [
      { time: '00:00', normal: 95, anomaly: 5 },
      { time: '04:00', normal: 98, anomaly: 2 },
      { time: '08:00', normal: 85, anomaly: 15 },
      { time: '12:00', normal: 90, anomaly: 10 },
      { time: '16:00', normal: 80, anomaly: 20 },
      { time: '20:00', normal: 88, anomaly: 12 }
    ],
    seasonalTrends: [
      { season: 'Spring', trips: 1200000, growth: 5.2 },
      { season: 'Summer', trips: 1350000, growth: 8.7 },
      { season: 'Fall', trips: 1180000, growth: 3.1 },
      { season: 'Winter', trips: 950000, growth: -2.4 }
    ],
    // New models
    surgePricing: [
      { zone: 'Manhattan', current_multiplier: 1.8, predicted_multiplier: 2.1, confidence: 85 },
      { zone: 'Brooklyn', current_multiplier: 1.2, predicted_multiplier: 1.4, confidence: 78 },
      { zone: 'Queens', current_multiplier: 1.0, predicted_multiplier: 1.1, confidence: 92 },
      { zone: 'Bronx', current_multiplier: 1.1, predicted_multiplier: 1.3, confidence: 80 },
      { zone: 'Staten Island', current_multiplier: 1.0, predicted_multiplier: 1.0, confidence: 95 }
    ],
    pickupHotspots: [
      { location: 'Times Square', cluster_size: 1200, density: 95 },
      { location: 'Penn Station', cluster_size: 980, density: 88 },
      { location: 'Union Square', cluster_size: 850, density: 82 },
      { location: 'Brooklyn Bridge', cluster_size: 720, density: 75 },
      { location: 'Central Park', cluster_size: 650, density: 70 }
    ],
    weatherImpact: [
      { condition: 'Clear', impact: 0, trips: 1000 },
      { condition: 'Light Rain', impact: -5, trips: 950 },
      { condition: 'Heavy Rain', impact: -15, trips: 850 },
      { condition: 'Snow', impact: -25, trips: 750 },
      { condition: 'Fog', impact: -10, trips: 900 }
    ],
    customerChurn: [
      { segment: 'Casual Users', churn_rate: 15, retention_cost: 12.5 },
      { segment: 'Regular Users', churn_rate: 8, retention_cost: 8.2 },
      { segment: 'Business Users', churn_rate: 3, retention_cost: 5.7 },
      { segment: 'Premium Users', churn_rate: 2, retention_cost: 3.1 }
    ],
    revenueForecast: [
      { month: 'Jan', actual: 2500000, predicted: 2450000, lower: 2300000, upper: 2600000 },
      { month: 'Feb', actual: 2300000, predicted: 2350000, lower: 2200000, upper: 2500000 },
      { month: 'Mar', actual: 2700000, predicted: 2750000, lower: 2600000, upper: 2900000 },
      { month: 'Apr', actual: 2600000, predicted: 2650000, lower: 2500000, upper: 2800000 },
      { month: 'May', actual: null, predicted: 2800000, lower: 2650000, upper: 2950000 },
      { month: 'Jun', actual: null, predicted: 2900000, lower: 2750000, upper: 3050000 }
    ]
  });

  // Colors for charts
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];
  const fraudColors = ['#00C9A7', '#FF6B6B'];
  const anomalyColors = ['#0088FE', '#FF6B6B'];
  const surgeColors = ['#FF6B6B', '#4ECDC4'];
  const churnColors = ['#FF6B6B', '#4ECDC4'];

  return (
    <div>
      <h1 className="section-title">Predictive Analytics</h1>
      
      <h2 className="section-title">Trip Demand Forecast</h2>
      <div className="card">
        <FullScreenChart title="Trip Demand Forecast">
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={predictiveData.demandForecast}
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
                  tick={{ fontSize: 12 }}
                  tickFormatter={formatNumber}
                />
                <Tooltip 
                  formatter={(value) => [formatNumber(value), 'Trips']}
                  labelFormatter={(value) => `Time: ${value}`}
                />
                <Legend />
                <Area 
                  type="monotone" 
                  dataKey="lower" 
                  name="Lower Bound" 
                  stroke="#8884d8" 
                  fill="#8884d8" 
                  fillOpacity={0.1} 
                  strokeOpacity={0.3}
                  activeDot={{ r: 6 }}
                />
                <Area 
                  type="monotone" 
                  dataKey="upper" 
                  name="Upper Bound" 
                  stroke="#8884d8" 
                  fill="#8884d8" 
                  fillOpacity={0.3} 
                  strokeOpacity={0.3}
                  activeDot={{ r: 6 }}
                />
                <Area 
                  type="monotone" 
                  dataKey="predicted" 
                  name="Predicted Demand" 
                  stroke="#8884d8" 
                  fill="#8884d8" 
                  fillOpacity={0.6} 
                  activeDot={{ r: 6 }}
                />
                <Line 
                  type="monotone" 
                  dataKey="actual" 
                  name="Actual Demand" 
                  stroke="#ff7300" 
                  strokeWidth={2}
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }} 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </FullScreenChart>
      </div>
      
      <div className="predictive-grid">
        <div className="card">
          <h3 className="card-title">Fare Fraud Detection</h3>
          <FullScreenChart title="Fare Fraud Detection">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={predictiveData.fraudDetection}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="count"
                    nameKey="type"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    activeIndex={0}
                  >
                    {predictiveData.fraudDetection.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={fraudColors[index % fraudColors.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    formatter={(value) => [formatNumber(value), 'Transactions']}
                  />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
        
        <div className="card">
          <h3 className="card-title">Traffic Congestion Model</h3>
          <FullScreenChart title="Traffic Congestion Model">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={predictiveData.congestion}
                  margin={{ top: 20, right: 30, left: 20, bottom: 40 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="route" 
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
                  <Bar dataKey="level" name="Current Level (%)" fill="#ff9e00" activeBar={{ fill: '#ff7700' }} />
                  <Bar dataKey="predicted" name="Predicted Level (%)" fill="#ff6b6b" activeBar={{ fill: '#ff3333' }} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
      </div>
      
      <h2 className="section-title">Route Optimization</h2>
      <div className="card">
        <FullScreenChart title="Route Optimization">
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={predictiveData.routeOptimization}
                margin={{ top: 20, right: 30, left: 20, bottom: 40 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="route" 
                  angle={-45}
                  textAnchor="end"
                  height={60}
                  tick={{ fontSize: 12 }}
                />
                <YAxis 
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => `${value} min`}
                />
                <Tooltip 
                  formatter={(value, name) => {
                    if (name === 'savings') {
                      return [`${value} min`, 'Time Savings'];
                    }
                    return [`${value} min`, name === 'current_time' ? 'Current Time' : 'Optimized Time'];
                  }}
                />
                <Legend />
                <Bar dataKey="current_time" name="Current Time" fill="#8884d8" activeBar={{ fill: '#5555ff' }} />
                <Bar dataKey="optimized_time" name="Optimized Time" fill="#00c9a7" activeBar={{ fill: '#009977' }} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </FullScreenChart>
      </div>
      
      <div className="predictive-grid">
        <div className="card">
          <h3 className="card-title">ML Model Performance</h3>
          <FullScreenChart title="ML Model Performance">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={predictiveData.modelPerformance}
                  margin={{ top: 20, right: 30, left: 20, bottom: 40 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="model" 
                    angle={-45}
                    textAnchor="end"
                    height={60}
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis 
                    yAxisId="accuracy"
                    domain={[0, 100]} 
                    tick={{ fontSize: 12 }}
                    tickFormatter={(value) => `${value}%`}
                    orientation="left"
                  />
                  <YAxis 
                    yAxisId="rmse"
                    domain={[0, 20]} 
                    tick={{ fontSize: 12 }}
                    orientation="right"
                  />
                  <Tooltip 
                    formatter={(value, name) => {
                      if (name === 'accuracy') {
                        return [`${value}%`, 'Accuracy'];
                      }
                      return [value, 'RMSE'];
                    }}
                  />
                  <Legend />
                  <Bar yAxisId="accuracy" dataKey="accuracy" name="Accuracy (%)" fill="#00c9a7" activeBar={{ fill: '#009977' }} />
                  <Bar yAxisId="rmse" dataKey="rmse" name="RMSE" fill="#ff6b6b" activeBar={{ fill: '#ff3333' }} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
        
        <div className="card">
          <h3 className="card-title">Anomaly Detection</h3>
          <FullScreenChart title="Anomaly Detection">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart
                  data={predictiveData.anomalyDetection}
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
                    tick={{ fontSize: 12 }}
                    tickFormatter={(value) => `${value}%`}
                  />
                  <Tooltip 
                    formatter={(value) => [`${value}%`, 'Percentage']}
                  />
                  <Legend />
                  <Area 
                    type="monotone" 
                    dataKey="normal" 
                    name="Normal Patterns" 
                    stackId="1" 
                    stroke="#8884d8" 
                    fill="#8884d8" 
                    fillOpacity={0.6} 
                    activeDot={{ r: 6 }}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="anomaly" 
                    name="Anomalies" 
                    stackId="1" 
                    stroke="#ff6b6b" 
                    fill="#ff6b6b" 
                    fillOpacity={0.6} 
                    activeDot={{ r: 6 }}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
      </div>
      
      <h2 className="section-title">Seasonal Trends</h2>
      <div className="card">
        <FullScreenChart title="Seasonal Trends">
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={predictiveData.seasonalTrends}>
                <PolarGrid />
                <PolarAngleAxis dataKey="season" />
                <PolarRadiusAxis />
                <Radar
                  name="Trips"
                  dataKey="trips"
                  stroke="#8884d8"
                  fill="#8884d8"
                  fillOpacity={0.6}
                  activeDot={{ r: 6 }}
                />
                <Tooltip 
                  formatter={(value) => [formatNumber(value), 'Trips']}
                />
                <Legend />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </FullScreenChart>
      </div>
      
      {/* New Models Section */}
      <h2 className="section-title">Additional Predictive Models</h2>
      
      <div className="predictive-grid">
        <div className="card">
          <h3 className="card-title">Surge Pricing Prediction</h3>
          <FullScreenChart title="Surge Pricing Prediction">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={predictiveData.surgePricing}
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
                    yAxisId="multiplier"
                    domain={[0, 3]} 
                    tick={{ fontSize: 12 }}
                    tickFormatter={(value) => `${value}x`}
                  />
                  <YAxis 
                    yAxisId="confidence"
                    domain={[0, 100]} 
                    tick={{ fontSize: 12 }}
                    orientation="right"
                    tickFormatter={(value) => `${value}%`}
                  />
                  <Tooltip 
                    formatter={(value, name) => {
                      if (name === 'confidence') {
                        return [`${value}%`, 'Confidence'];
                      }
                      return [`${value}x`, 'Multiplier'];
                    }}
                  />
                  <Legend />
                  <Bar yAxisId="multiplier" dataKey="current_multiplier" name="Current Multiplier" fill="#ff9e00" activeBar={{ fill: '#ff7700' }} />
                  <Bar yAxisId="multiplier" dataKey="predicted_multiplier" name="Predicted Multiplier" fill="#ff6b6b" activeBar={{ fill: '#ff3333' }} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
        
        <div className="card">
          <h3 className="card-title">Pickup Hotspot Clustering</h3>
          <FullScreenChart title="Pickup Hotspot Clustering">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart
                  margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
                >
                  <CartesianGrid />
                  <XAxis 
                    type="number" 
                    dataKey="cluster_size" 
                    name="Cluster Size" 
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis 
                    type="number" 
                    dataKey="density" 
                    name="Density" 
                    domain={[0, 100]}
                    tick={{ fontSize: 12 }}
                    tickFormatter={(value) => `${value}%`}
                  />
                  <Tooltip 
                    cursor={{ strokeDasharray: '3 3' }}
                    formatter={(value, name) => {
                      if (name === 'density') {
                        return [`${value}%`, 'Density'];
                      }
                      return [formatNumber(value), 'Trips'];
                    }}
                  />
                  <Legend />
                  <Scatter 
                    name="Hotspots" 
                    data={predictiveData.pickupHotspots} 
                    fill="#8884d8" 
                    activeDot={{ r: 8 }}
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
      </div>
      
      <div className="predictive-grid">
        <div className="card">
          <h3 className="card-title">Weather Impact Analysis</h3>
          <FullScreenChart title="Weather Impact Analysis">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={predictiveData.weatherImpact}
                  margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="condition" 
                    angle={-45}
                    textAnchor="end"
                    height={60}
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis 
                    yAxisId="impact"
                    domain={[-30, 10]} 
                    tick={{ fontSize: 12 }}
                    tickFormatter={(value) => `${value}%`}
                  />
                  <YAxis 
                    yAxisId="trips"
                    orientation="right"
                    tick={{ fontSize: 12 }}
                    tickFormatter={formatNumber}
                  />
                  <Tooltip 
                    formatter={(value, name) => {
                      if (name === 'impact') {
                        return [`${value}%`, 'Impact on Trips'];
                      }
                      return [formatNumber(value), 'Trips'];
                    }}
                  />
                  <Legend />
                  <Bar yAxisId="impact" dataKey="impact" name="Impact (%)" fill="#ff6b6b" activeBar={{ fill: '#ff3333' }} />
                  <Bar yAxisId="trips" dataKey="trips" name="Trips" fill="#8884d8" activeBar={{ fill: '#5555ff' }} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
        
        <div className="card">
          <h3 className="card-title">Customer Churn Prediction</h3>
          <FullScreenChart title="Customer Churn Prediction">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={predictiveData.customerChurn}
                  margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="segment" 
                    angle={-45}
                    textAnchor="end"
                    height={60}
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis 
                    yAxisId="churn"
                    domain={[0, 20]} 
                    tick={{ fontSize: 12 }}
                    tickFormatter={(value) => `${value}%`}
                  />
                  <YAxis 
                    yAxisId="cost"
                    orientation="right"
                    tick={{ fontSize: 12 }}
                    tickFormatter={(value) => `$${value}`}
                  />
                  <Tooltip 
                    formatter={(value, name) => {
                      if (name === 'churn_rate') {
                        return [`${value}%`, 'Churn Rate'];
                      }
                      return [`$${value}`, 'Retention Cost'];
                    }}
                  />
                  <Legend />
                  <Bar yAxisId="churn" dataKey="churn_rate" name="Churn Rate (%)" fill="#ff6b6b" activeBar={{ fill: '#ff3333' }} />
                  <Bar yAxisId="cost" dataKey="retention_cost" name="Retention Cost ($)" fill="#4ECDC4" activeBar={{ fill: '#22aaaa' }} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </FullScreenChart>
        </div>
      </div>
      
      <h2 className="section-title">Revenue Forecast</h2>
      <div className="card">
        <FullScreenChart title="Revenue Forecast">
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={predictiveData.revenueForecast}
                margin={{ top: 20, right: 30, left: 20, bottom: 40 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="month" 
                  angle={-45}
                  textAnchor="end"
                  height={60}
                  tick={{ fontSize: 12 }}
                />
                <YAxis 
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => `$${formatNumber(value)}`}
                />
                <Tooltip 
                  formatter={(value) => [`$${formatNumber(value)}`, 'Revenue']}
                  labelFormatter={(value) => `Month: ${value}`}
                />
                <Legend />
                <Area 
                  type="monotone" 
                  dataKey="lower" 
                  name="Lower Bound" 
                  stroke="#8884d8" 
                  fill="#8884d8" 
                  fillOpacity={0.1} 
                  strokeOpacity={0.3}
                  activeDot={{ r: 6 }}
                />
                <Area 
                  type="monotone" 
                  dataKey="upper" 
                  name="Upper Bound" 
                  stroke="#8884d8" 
                  fill="#8884d8" 
                  fillOpacity={0.3} 
                  strokeOpacity={0.3}
                  activeDot={{ r: 6 }}
                />
                <Area 
                  type="monotone" 
                  dataKey="predicted" 
                  name="Predicted Revenue" 
                  stroke="#8884d8" 
                  fill="#8884d8" 
                  fillOpacity={0.6} 
                  activeDot={{ r: 6 }}
                />
                <Line 
                  type="monotone" 
                  dataKey="actual" 
                  name="Actual Revenue" 
                  stroke="#ff7300" 
                  strokeWidth={2}
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }} 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </FullScreenChart>
      </div>
    </div>
  );
};

export default Predictive;