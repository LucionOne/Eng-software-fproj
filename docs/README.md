# Garden Manager

**Author:** Guilherme P. Santos (209635)

## Overview
A lightweight garden monitoring and management system consisting of three components: a Python-based manager (data aggregation & API), a mock sensor simulator, and a web dashboard. Designed for local deployment with persistent SQLite storage.

## Architecture
- **Manager:** FastAPI server with SQLite database and threaded data ingestion
- **Mock API:** Simulates IoT sensor data (temperature, humidity, soil moisture, etc.)
- **Dashboard:** Web-based UI for real-time garden monitoring and analytics

## Quick Start

### Prerequisites
- Python 3.8+
- `requests` library

### Installation
```bash
pip install -r requirements.txt
python src/Main.py
```

### Access
- API: `http://localhost:3002`
- Dashboard: `http://localhost:3002` (root returns dashboard HTML)

## Project Structure
```
src/
├── Main.py                    # Entry point
├── classes/
│   ├── DatabaseManager.py     # SQLite connection & query operations
│   ├── dataPuller.py          # Sensor data ingestion with validation
│   └── APIService.py          # FastAPI server & endpoints
├── lib/
│   └── logger.py              # Logging utilities
└── assets/
    ├── dashboard.html         # Web-based monitoring UI
    ├── SQL_config.py          # Database schema & initialization
    └── data_logs_db_wireframe.sql
tests/
├── test_*.py                  # Unit tests for core components
```

## Tech Stack
- **Language:** Python 3
- **Backend:** FastAPI
- **Database:** SQLite3
- **Threading:** Python `threading` module
- **Frontend:** HTML/JavaScript (planned)

## Key Features

### Data Ingestion & Validation
- Real-time sensor data pulling from mock API (configurable)
- Input validation at the boundary: rejects out-of-range readings (e.g., pH 0-14, humidity 0-100, temperature -50 to 60°C)
- ISO 8601 datetime format validation
- Failed validations logged without corrupting the database

### API Endpoints
- `GET /` – Returns dashboard HTML
- `GET /data` – Fetch all sensor readings
- `GET /data?after_id=N` – Fetch readings after ID N for incremental updates

## Development
- **Process:** See `docs/other/Process.md` for DoR/DoD and workflow
- **Architecture:** See `docs/architecture/architectureOfAll.md` for detailed design
- **Backlog:** See `docs/other/Backlog.md` for feature requirements
- **Objectives:** See `Objectives.md` for current sprint goals

## Repository
https://github.com/LucionOne/Eng-software-fproj.git