# NYC TLC Data Flow

```mermaid
graph TD
    A[NYC Open Data Portal] --> B[Taxi Data Extractor]
    B --> C[ETL Pipeline]
    C --> D[Data Transformation]
    D --> E[Data Loading]
    E --> F[Analytics Warehouse]
    
    subgraph API Layer
        G[Taxi Metadata API]
        H[Taxi Trips API]
        I[Historical Data API]
        J[Transform API]
        K[Load API]
    end
    
    B --> G
    B --> H
    B --> I
    C --> J
    C --> K
    E --> F
```

## NYC TLC API Endpoints

### Metadata
- `GET /api/v1/taxi/metadata` - Get dataset metadata

### Data Access
- `GET /api/v1/taxi/trips` - Get taxi trip data
- `GET /api/v1/taxi/historical` - Get historical taxi data

### Processing
- `POST /api/v1/taxi/transform` - Transform raw taxi data
- `POST /api/v1/taxi/load` - Load transformed data to warehouse