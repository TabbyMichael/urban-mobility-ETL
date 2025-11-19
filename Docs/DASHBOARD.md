# Urban Mobility Analytics Dashboard

A React-based dashboard for visualizing urban mobility and transportation analytics data.

## Features

### Dashboard Overview
- Key metrics display (average fare, total trips, peak hour, top pickup zone)
- Trip volume by hour visualization
- Peak pickup zones pie chart
- Fare distribution analysis

### Analytics
- Detailed trip volume analysis with line charts
- Pickup zone comparison with bar charts
- Comprehensive fare analysis
- Fraud detection visualization

### Maps
- Interactive map with pickup hotspots
- Congestion levels visualization
- Surge pricing zones analysis

### Predictive Analytics
- Trip demand forecasting
- Fare fraud detection models
- Traffic congestion modeling
- ML model performance metrics

## Technologies Used

- **Frontend**: React, Vite
- **Charts**: Recharts
- **Maps**: Leaflet, React-Leaflet
- **Routing**: React Router
- **Backend Proxy**: Express, http-proxy-middleware

## Setup Instructions

1. Install dependencies:
   ```bash
   cd dashboard
   npm install
   ```

2. Build the dashboard:
   ```bash
   npm run build
   ```

3. Start the proxy server:
   ```bash
   cd ..
   node server.js
   ```

4. Access the dashboard at http://localhost:3000

## Development

To run in development mode:
```bash
cd dashboard
npm run dev
```

The dashboard will be available at http://localhost:3001 (or another port if 3001 is in use).

## API Integration

The dashboard connects to the Flask backend API through a proxy:
- Dashboard requests to `/api/*` are forwarded to `http://localhost:5000/api/v1/*`

## Components

- `Dashboard.jsx` - Main overview with key metrics
- `Analytics.jsx` - Detailed analytics visualizations
- `Maps.jsx` - Geospatial analytics with interactive maps
- `Predictive.jsx` - Machine learning and predictive models