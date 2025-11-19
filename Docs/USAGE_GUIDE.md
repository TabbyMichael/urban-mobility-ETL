# Usage Guide: Urban Mobility & Transportation Analytics ETL

This guide explains how to use all the newly implemented features in the Urban Mobility Analytics platform.

## 1. Database Setup

### Initialize the Database Schema
```bash
# Run the database initialization script
python init_database.py
```

This will create all necessary tables in your PostgreSQL database with PostGIS support.

### Database Schema Overview
- `trips`: Taxi trip data with spatial columns
- `zones`: Taxi zone reference data
- `weather`: Weather data for analytics
- `uber_travel_times`: Uber Movement travel time data
- `mta_status`: MTA transit status data
- `features_ml`: Preprocessed features for machine learning
- `users`: User authentication data

## 2. Authentication System

### User Registration
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "securepassword",
    "role": "user"
  }'
```

### User Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

Response:
```json
{
  "message": "Login successful",
  "username": "admin",
  "role": "admin",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Using Authentication Tokens
Include the token in the Authorization header for all protected endpoints:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  http://localhost:5000/api/v1/taxi/trips?limit=10
```

## 3. Real-time Data Streaming

### Connecting to the WebSocket Server
The real-time streaming is available at `ws://localhost:5000/socket.io/`.

### JavaScript Client Example
```javascript
import io from 'socket.io-client';

// Connect to the server
const socket = io('http://localhost:5000');

// Listen for connection
socket.on('connect', () => {
  console.log('Connected to real-time stream');
  
  // Start streaming
  socket.emit('start_streaming', {
    dataset_id: 't29m-gskq',
    interval: 5
  });
});

// Listen for taxi data
socket.on('taxi_data', (data) => {
  console.log('New taxi data:', data);
});

// Listen for analytics data
socket.on('analytics_data', (data) => {
  console.log('Analytics update:', data);
});

// Stop streaming
socket.emit('stop_streaming');
```

## 4. Data Source APIs

### NYC Taxi Data
```bash
# Get taxi trip data
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:5000/api/v1/taxi/trips?limit=10&dataset_id=t29m-gskq"

# Get historical data
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:5000/api/v1/taxi/historical?months=3"
```

### Uber Movement Data
```bash
# Get travel times
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:5000/api/v1/uber/travel-times?source_id=1001&dst_id=2001"

# Get speed data
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:5000/api/v1/uber/speeds?city_id=1"
```

### MTA Transit Data
```bash
# Get real-time transit data
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:5000/api/v1/transit/realtime?feed_id=1"

# Get service alerts
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:5000/api/v1/transit/alerts"
```

## 5. Dashboard Navigation

### New Real-time Analytics Page
Visit `http://localhost:3000/realtime` to access the real-time analytics dashboard.

The dashboard includes:
- Connection status indicators
- Live trip visualization on map
- Real-time trip volume charts
- Fare distribution analytics

### Other Dashboard Pages
- **Dashboard**: `http://localhost:3000/` - Key metrics overview
- **Analytics**: `http://localhost:3000/analytics` - Detailed data visualizations
- **Maps**: `http://localhost:3000/maps` - Interactive geospatial analytics
- **Predictive**: `http://localhost:3000/predictive` - Machine learning models and forecasts

## 6. Health Monitoring

### System Health Check
```bash
# Overall system health
curl http://localhost:5000/api/v1/health

# Database-specific health
curl http://localhost:5000/api/v1/health/database

# Authentication system health
curl http://localhost:5000/api/v1/health/auth
```

Sample health response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-08T10:30:45.123456",
  "components": {
    "database": {
      "status": "healthy",
      "component": "database",
      "message": "Database is healthy",
      "query_time_ms": 15.23
    },
    "authentication": {
      "status": "healthy",
      "component": "authentication",
      "message": "Authentication system is healthy"
    }
  }
}
```

## 7. Running the Application

### Backend Server
```bash
# Start the backend server with real-time streaming support
python run.py
```

### Frontend Dashboard
```bash
# Navigate to dashboard directory
cd dashboard

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

### Environment Variables
Create a `.env` file in the root directory:
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=urban_mobility
DB_USER=postgres
DB_PASSWORD=your_secure_password

# Security Configuration
SECRET_KEY=your_production_secret_key
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=your_hashed_admin_password

# API Keys (for external data sources)
UBER_MOVEMENT_API_KEY=your_uber_api_key
MTA_API_KEY=your_mta_api_key

# API Configuration
FLASK_ENV=production
FLASK_DEBUG=False
```

## 8. Testing the Implementation

### Run Authentication Tests
```bash
python test_auth.py
```

### Run Database Tests
```bash
python test_database.py
```

### Run Streaming Tests
```bash
python test_streaming.py
```

## 9. Deployment

### Backend Deployment (Railway)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy
railway up
```

### Frontend Deployment (Vercel)
```bash
# Navigate to dashboard
cd dashboard

# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

## 10. Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify PostgreSQL is running
   - Check database credentials in `.env` file
   - Ensure PostGIS extension is installed

2. **Authentication Errors**
   - Verify SECRET_KEY is set in `.env`
   - Check that users table was created during initialization

3. **Real-time Streaming Not Working**
   - Ensure SocketIO server is running
   - Check browser console for WebSocket connection errors
   - Verify CORS settings

4. **Dashboard Not Loading**
   - Ensure backend server is running
   - Check network tab for API connection errors
   - Verify authentication token is valid

### Getting Help
For issues not covered in this guide, check:
- Application logs in the `logs/` directory
- Database logs for connection issues
- Browser developer console for frontend errors