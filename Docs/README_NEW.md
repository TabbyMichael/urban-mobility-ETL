# Urban Mobility & Transportation Analytics ETL

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.2.5-green)
![React](https://img.shields.io/badge/React-18.2.0-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen)

A unified data pipeline that extracts, transforms, and loads NYC taxi, Uber, and public transit data into an analytical warehouse for traffic pattern analysis, ride demand prediction, and anomaly detection. Features a responsive React dashboard with interactive visualizations.

## Features

### 🚇 ETL Pipeline
- **Multi-source Data Integration**: Extracts data from NYC TLC, Uber Movement, and MTA GTFS
- **Automated Data Processing**: Transforms raw data into analytical formats
- **Gold Layer Storage**: Loads final tables into PostgreSQL with PostGIS for spatial queries
- **Workflow Orchestration**: Apache Airflow DAG for automated ETL execution

### 🔐 Security Features
- **Authentication**: JWT-based authentication for API endpoints
- **Authorization**: Role-based access control for different user types
- **Input Validation**: JSON validation and size limits to prevent abuse
- **Environment Configuration**: Secure credential management through environment variables

### 📊 Analytics Dashboard
- **Interactive Visualizations**: Real-time charts and graphs using Recharts
- **Geospatial Mapping**: Interactive maps with Leaflet for pickup hotspots and congestion zones
- **Predictive Analytics**: Machine learning models for demand forecasting and fraud detection
- **Fully Responsive**: Works on mobile, tablet, desktop, and large displays

### 🔍 Advanced Analytics
- **Descriptive Analytics**: Trip volume analysis, peak zones, fare distribution
- **Predictive Modeling**: Random Forest for demand forecasting, Isolation Forest for fraud detection
- **Spatial Analytics**: DBSCAN clustering for pickup hotspots, route optimization algorithms

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL with PostGIS extension
- Virtual environment tool (venv or conda)

### Backend Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd urban-mobility-analytics
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL with PostGIS:
   ```bash
   # Install PostgreSQL and PostGIS
   sudo apt install postgresql postgis
   
   # Create database and user
   sudo -u postgres createdb urban_mobility
   sudo -u postgres createuser -s postgres
   
   # Set password for postgres user
   sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
   
   # Connect to database and enable PostGIS
   sudo -u postgres psql -d urban_mobility -c "CREATE EXTENSION IF NOT EXISTS postgis;"
   ```

5. Create a `.env` file from the template:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

6. Initialize database tables:
   ```bash
   python init_database.py
   ```

### Frontend Setup

1. Install Node.js dependencies:
   ```bash
   cd dashboard
   npm install
   ```

2. Build the React dashboard:
   ```bash
   npm run build
   cd ..
   ```

## Usage Examples

### Running the Application

1. Start the Flask backend:
   ```bash
   python run.py
   ```

2. In a separate terminal, start the dashboard server:
   ```bash
   node server.js
   ```

3. Access the dashboard at `http://localhost:3000`

### API Authentication

All API endpoints require authentication. First, obtain a token:

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'
```

Use the token in subsequent requests:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  http://localhost:5000/api/v1/taxi/trips?limit=10
```

### API Endpoints

```bash
# Health check
curl http://localhost:5000/api/v1/health

# Get taxi trip data (requires authentication)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/v1/taxi/trips?limit=10

# Get Uber data (requires authentication)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/v1/uber

# Get transit data (requires authentication)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/v1/transit
```

### Dashboard Navigation

- **Dashboard** (`/`): Key metrics overview
- **Analytics** (`/analytics`): Detailed data visualizations
- **Maps** (`/maps`): Interactive geospatial analytics
- **Predictive** (`/predictive`): Machine learning models and forecasts

## Configuration

### Environment Variables

Create a `.env` file in the root directory (see `.env.example`):

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=urban_mobility
DB_USER=postgres
DB_PASSWORD=your_secure_password

# Security Configuration
SECRET_KEY=your_secret_key_here
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=your_hashed_password_here

# API Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

## Tech Stack

### Backend
- **Flask** - Web framework for RESTful APIs
- **Pandas** - Data processing and analysis
- **SQLAlchemy** - Database ORM
- **PostgreSQL + PostGIS** - Spatial database
- **Scikit-learn** - Machine learning algorithms
- **Apache Airflow** - Workflow orchestration
- **JWT** - Authentication and authorization

### Frontend
- **React** - UI framework
- **Vite** - Build tool and development server
- **Recharts** - Data visualization library
- **Leaflet + React-Leaflet** - Interactive mapping
- **React Router** - Client-side routing
- **Express** - Proxy server

### Data Sources
- **NYC TLC Data** - Taxi & Limousine Commission via NYC Open Data Portal
- **Uber Movement** - Aggregated travel times API
- **MTA GTFS** - Real-time transit feeds

## Testing

### Backend Testing
```bash
# Run all tests
python run_all_tests.py

# Run API tests
python test_api.py

# Run ETL pipeline tests
python test_etl_pipeline.py
```

### Frontend Testing
```bash
cd dashboard

# Run linting
npm run lint

# Run in development mode
npm run dev
```

## Deployment

### Railway Deployment (Backend API)

This project is configured for easy deployment to Railway with PostgreSQL and PostGIS support.

1. Install the Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Initialize a new Railway project:
   ```bash
   railway init
   ```

4. Add PostgreSQL with PostGIS:
   ```bash
   railway add postgresql
   ```

5. Deploy the application:
   ```bash
   railway up
   ```

The deployment will automatically:
- Use the `railway.toml` configuration
- Start the Flask application on the port specified by Railway
- Connect to the PostgreSQL database with PostGIS
- Set up environment variables automatically

### Vercel Deployment (Frontend Dashboard)

The React dashboard is configured for deployment to Vercel.

1. Install the Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Navigate to the dashboard directory:
   ```bash
   cd dashboard
   ```

3. Login to Vercel:
   ```bash
   vercel login
   ```

4. Deploy the project:
   ```bash
   vercel --prod
   ```

The deployment will automatically:
- Use the `vercel.json` configuration
- Build the React application with Vite
- Deploy to a global CDN
- Set up automatic SSL

### Deployment Scripts

For easier deployment, you can use the provided scripts:

```bash
# Deploy backend to Railway
./deploy_railway.sh

# Deploy frontend to Vercel
./dashboard/deploy_vercel.sh
```

## Contribution Guidelines

### Getting Started
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Commit your changes: `git commit -m 'Add new feature'`
5. Push to the branch: `git push origin feature-name`
6. Create a pull request

### Code Standards
- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/JSX
- Write docstrings for all functions and classes
- Include unit tests for new functionality

### Reporting Issues
- Use the GitHub issue tracker
- Include detailed steps to reproduce
- Provide environment information
- Tag issues appropriately (bug, enhancement, question)

## Roadmap

### Short-term Goals
- [ ] Add real-time data streaming capabilities
- [ ] Implement additional ML models for predictive analytics
- [ ] Enhance dashboard with more interactive filters
- [ ] Add user authentication and authorization

### Medium-term Goals
- [ ] Integrate additional data sources (bike shares, scooters)
- [ ] Develop mobile application
- [ ] Add export functionality for reports
- [ ] Implement advanced anomaly detection algorithms

### Long-term Goals
- [ ] Create public API for external developers
- [ ] Add support for other cities
- [ ] Implement deep learning models
- [ ] Develop recommendation engine for route optimization

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [NYC Taxi & Limousine Commission](https://www.nyc.gov/html/tlc/html/home/home.shtml) for providing the taxi data
- [Uber Movement](https://movement.uber.com/) for travel time data
- [MTA](https://new.mta.info/) for public transit data
- [OpenStreetMap](https://www.openstreetmap.org/) for map data
- All contributors who have helped develop and improve this project