# System Architecture

## Overview
Three-tier system: data source (mock API) → manager (aggregation & storage) → dashboard (UI).

```
┌──────────────┐
│  Mock API    │ (Sensor data simulator)
└──────┬───────┘
       │ HTTP
       ▼
┌──────────────────────────────────────┐
│     Manager (FastAPI)                │
├──────────────────────────────────────┤
│  • DataPuller (threaded ingestion)   │
│  • DatabaseManager (SQLite ops)      │
│  • REST API (data export)            │
└──────┬───────────────────────────────┘
       │ HTTP
       ▼
┌──────────────────┐
│   Dashboard      │ (HTML/JS)
└──────────────────┘
```

## Components

### 1. Mock API
- **Purpose:** Simulate IoT sensor data (temperature, humidity, soil moisture, etc.)
- **Implementation:** Python HTTP server or JSON Server
- **Output:** JSON endpoints returning realistic garden sensor readings

### 2. Manager (Core)
- **Framework:** FastAPI (fast, async-ready, minimal overhead)
- **Database:** SQLite3 (simple, file-based, no external dependencies)
- **Concurrency:** Python `threading` for parallel data ingestion

**Key Classes:**
- `DatabaseManager` — Initialize, query, and persist data to SQLite
- `DataPuller` — Threaded ingestion from mock API at regular intervals
- `API Routes` — Expose aggregated data for dashboard consumption

### 3. Dashboard
- **Type:** Static HTML/JavaScript SPA (single-page application)
- **Integration:** Fetches data from manager via REST API
- **Deployment:** Served by FastAPI static file handler

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Python | Rapid development, sufficient for non-scaled projects |
| FastAPI | Type-safe, auto-docs, minimal setup |
| SQLite | Zero external dependencies, perfect for single-instance local use |
| Threading | Lightweight concurrency without async complexity for initial phase |
| Static HTML/JS | Simplicity; no separate frontend server required |

## Data Flow
1. **Polling:** DataPuller threads wake on schedule
2. **Fetch:** Pull sensor data from mock API
3. **Store:** Write to SQLite via DatabaseManager
4. **Serve:** Dashboard queries manager API
5. **Display:** Frontend renders real-time metrics

## Future Considerations
- Async/await refactor if scaling needed
- Add database indexing for large datasets
- Implement caching for frequently-accessed metrics
- Containerize with Docker for deployment