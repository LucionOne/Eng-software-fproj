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
- API: `http://localhost:8000`
- Dashboard: `http://localhost:8000/dashboard` (when implemented)

## Project Structure
```
src/
├── Main.py           # Entry point
├── classes/          # Core business logic (DatabaseManager, DataPuller, etc.)
├── lib/              # Utility functions
└── assets/           # Static files for dashboard
```

## Tech Stack
- **Language:** Python 3
- **Backend:** FastAPI
- **Database:** SQLite3
- **Threading:** Python `threading` module
- **Frontend:** HTML/JavaScript (planned)

## Development
- **Process:** See `docs/other/Process.md` for DoR/DoD and workflow
- **Architecture:** See `docs/architecture/architectureOfAll.md` for detailed design
- **Backlog:** See `docs/other/Backlog.md` for feature requirements

## Repository
https://github.com/LucionOne/Eng-software-fproj.git