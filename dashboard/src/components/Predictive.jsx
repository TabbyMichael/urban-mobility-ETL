import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area, PieChart, Pie, Cell, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';

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
    ]
  });

  // Colors for charts
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];
  const fraudColors = ['#00C9A7', '#FF6B6B'];
  const anomalyColors = ['#0088FE', '#FF6B6B'];

  return (
    <div>
      <h1 className="section-title">Predictive Analytics</h1>
      
      <h2 className="section-title">Trip Demand Forecast</h2>
      <div className="card">
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
              />
              <Area 
                type="monotone" 
                dataKey="upper" 
                name="Upper Bound" 
                stroke="#8884d8" 
                fill="#8884d8" 
                fillOpacity={0.3} 
                strokeOpacity={0.3}
              />
              <Area 
                type="monotone" 
                dataKey="predicted" 
                name="Predicted Demand" 
                stroke="#8884d8" 
                fill="#8884d8" 
                fillOpacity={0.6} 
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
      </div>
      
      <div className="predictive-grid">
        <div className="card">
          <h3 className="card-title">Fare Fraud Detection</h3>
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
        </div>
        
        <div className="card">
          <h3 className="card-title">Traffic Congestion Model</h3>
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
                <Bar dataKey="level" name="Current Level (%)" fill="#ff9e00" />
                <Bar dataKey="predicted" name="Predicted Level (%)" fill="#ff6b6b" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      
      <h2 className="section-title">Route Optimization</h2>
      <div className="card">
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
              <Bar dataKey="current_time" name="Current Time" fill="#8884d8" />
              <Bar dataKey="optimized_time" name="Optimized Time" fill="#00c9a7" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      <div className="predictive-grid">
        <div className="card">
          <h3 className="card-title">ML Model Performance</h3>
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
                <Bar yAxisId="accuracy" dataKey="accuracy" name="Accuracy (%)" fill="#00c9a7" />
                <Bar yAxisId="rmse" dataKey="rmse" name="RMSE" fill="#ff6b6b" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="card">
          <h3 className="card-title">Anomaly Detection</h3>
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
                />
                <Area 
                  type="monotone" 
                  dataKey="anomaly" 
                  name="Anomalies" 
                  stackId="1" 
                  stroke="#ff6b6b" 
                  fill="#ff6b6b" 
                  fillOpacity={0.6} 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      
      <h2 className="section-title">Seasonal Trends</h2>
      <div className="card">
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
              />
              <Tooltip 
                formatter={(value) => [formatNumber(value), 'Trips']}
              />
              <Legend />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Predictive;