# Backlog v0.1 — Garden Manager

## Overview
Core feature set for MVP: persistent data logging from sensors and real-time dashboard access.

## Functional Requirements (FR)

**FR1 — Data Logging** *(Must Have)*
- System must ingest sensor data from mock API at regular intervals
- Data must be persisted to SQLite database with timestamps
- Supported metrics: temperature, humidity, soil moisture, light level

**FR2 — Data API** *(Must Have)*
- System must expose REST endpoints for dashboard consumption
- Endpoints must support filtering by date range and metric type
- Response format: JSON with proper error handling

**FR3 — Dashboard** *(Nice to Have)*
- Real-time visualization of current sensor readings
- Historical charts (past 24 hours, past 7 days)
- Alert indicators for out-of-range values

## Non-Functional Requirements (NFR)

| Requirement | Target |
|------------|--------|
| Availability | 24/7 uptime during operation |
| Latency | <500ms API response time |
| Storage | SQLite, no external DB required |
| Scalability | Single-instance, supports ~1M records |
| Security | None required for MVP (local use only) |

## Constraints

- **No external paid libraries:** Open-source or Python standard library only
- **Single-server deployment:** No distributed systems complexity
- **Local network only:** No public internet exposure required
- **Development time:** <1 week for MVP

## Acceptance Criteria
- [ ] DataPuller pulls data every 5 minutes without errors
- [ ] 1000+ records can be stored and queried in <500ms
- [ ] Dashboard displays current readings and 24-hour history
- [ ] System remains stable for 24-hour test run
