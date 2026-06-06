# Next Steps Roadmap

**Last Updated:** 2026-06-06  
**Target Completion:** <7 days  
**Current Status:** DatabaseManager ✓ | DataPuller in progress

---

## Phase 1: Core Manager (2-3 days) — CRITICAL

### 1.1 Complete DataPuller Class
**Status:** In progress  
**Estimated:** 2-3 hours  
**Tasks:**
- [ ] Finalize URL configuration for mock API endpoints
- [ ] Implement threaded polling loop (5-minute intervals)
- [ ] Add error handling for network timeouts
- [ ] Connect to DatabaseManager for persistence
- [ ] Write unit tests

**Acceptance Criteria:**
- DataPuller successfully polls mock API
- Data persists to SQLite without corruption
- Threads handle graceful shutdown

---

### 1.2 Set Up Mock API Server
**Status:** Not started  
**Estimated:** 2 hours  
**Blocked by:** DataPuller URL config finalized

**Tasks:**
- [ ] Choose implementation: Python HTTP server or JSON Server
- [ ] Define sensor data endpoints (e.g., `/sensors/temperature`, `/sensors/humidity`)
- [ ] Generate realistic garden data (temp: 15-30°C, humidity: 30-90%, soil moisture: 20-80%)
- [ ] Add timestamp to all responses
- [ ] Optional: Add data variation patterns (daily cycles, etc.)

**Endpoint Examples:**
```
GET /api/sensors/current
{
  "timestamp": "2026-06-06T18:24:33Z",
  "temperature": 24.5,
  "humidity": 65,
  "soil_moisture": 52,
  "light_level": 8000
}

GET /api/sensors/history?metric=temperature&hours=24
[...]
```

---

## Phase 2: API Layer (1-2 days) — HIGH

### 2.1 Implement REST API Routes
**Status:** Not started  
**Estimated:** 3-4 hours  
**Blocked by:** DataPuller ✓, Mock API ✓

**Tasks:**
- [ ] Add FastAPI routes to existing main application
- [ ] Implement `GET /api/sensors/current` (latest readings)
- [ ] Implement `GET /api/data?from=ISO8601&to=ISO8601` (query by date range)
- [ ] Add filtering by metric type (temperature, humidity, etc.)
- [ ] Include proper HTTP status codes and error messages
- [ ] Write route integration tests

**Response Format:**
```json
{
  "status": "success",
  "timestamp": "2026-06-06T18:24:33Z",
  "data": [
    {"timestamp": "...", "metric": "temperature", "value": 24.5},
    ...
  ],
  "count": 42
}
```

---

## Phase 3: Dashboard (1-2 days) — HIGH

### 3.1 Build Dashboard UI
**Status:** Not started  
**Estimated:** 4-5 hours  
**Blocked by:** API Layer ✓

**Tasks:**
- [ ] Create `src/assets/dashboard.html`
- [ ] Add real-time sensor readout section (current temperature, humidity, soil moisture)
- [ ] Implement chart.js or similar for historical data visualization
- [ ] Add date range picker for filtering
- [ ] Fetch data from `/api/data` on page load and every 30 seconds
- [ ] Include status indicators (online/offline, warning zones)
- [ ] Responsive design (mobile-friendly)

**Minimum Features:**
- Current readings with units (°C, %, etc.)
- Last 24 hours chart (line graph)
- Last 7 days summary (optional)
- Refresh status and timestamp

---

## Phase 4: Testing & Optimization (1 day) — HIGH

### 4.1 Integration Testing
**Status:** Not started  
**Estimated:** 3-4 hours  
**Blocked by:** Dashboard ✓

**Tests to Write:**
- [ ] End-to-end: Mock API → DataPuller → Database → API → Dashboard
- [ ] Database: Query performance with 1000+ records
- [ ] API: Response times <500ms under normal load
- [ ] Dashboard: Data loads and updates correctly
- [ ] Error scenarios: Network loss, database errors, invalid queries

**Test Command:**
```bash
python -m pytest tests/ -v
```

---

### 4.2 Performance & Stability
**Status:** Not started  
**Estimated:** 2-3 hours  
**Blocked by:** Integration Tests ✓

**Tasks:**
- [ ] Add database indexing on timestamp column
- [ ] Profile DataPuller memory usage over 24 hours
- [ ] Implement graceful shutdown (SIGTERM handling)
- [ ] Add logging for debugging
- [ ] Run 24-hour stability test with mock API running continuously
- [ ] Document any issues found and fixes applied

**Success Criteria:**
- No memory leaks after 24h continuous operation
- API response time remains <500ms
- Zero data loss
- Graceful recovery from network interruptions

---

## Phase 5: Deployment & Documentation (Final) — MEDIUM

### 5.1 Deployment Setup
**Status:** Not started  
**Estimated:** 1-2 hours

**Tasks:**
- [ ] Create `requirements.txt` with all dependencies
- [ ] Add `start.sh` script for easy startup
- [ ] Document environment variables (if any)
- [ ] Update README.md with final setup steps
- [ ] Create systemd service file (optional, for auto-start)

---

### 5.2 Final Documentation
**Status:** In progress (docs refresh complete)  
**Tasks:**
- [x] Update README with project overview and quick start
- [x] Formalize architecture documentation
- [x] Clarify development process
- [x] Document tech stack decisions
- [ ] Add deployment guide
- [ ] Add troubleshooting section

---

## Dependencies & Blocking Order

```
Phase 1.1 (DataPuller) 
    ↓
Phase 1.2 (Mock API) 
    ↓
Phase 2.1 (API Routes)
    ↓
Phase 3.1 (Dashboard)
    ↓
Phase 4.1 (Integration Tests)
    ↓
Phase 4.2 (Optimization)
    ↓
Phase 5 (Deployment)
```

---

## Daily Targets

| Day | Target |
|-----|--------|
| Day 1-2 | ✓ DataPuller + Mock API integration complete |
| Day 3 | API routes implemented and tested |
| Day 4 | Dashboard UI complete and connected |
| Day 5 | Integration tests passing |
| Day 6 | Performance testing and optimization |
| Day 7 | Final polish, deployment docs, contingency buffer |

---

## Success Metrics
- [ ] System runs 24 hours without errors
- [ ] DataPuller polls mock API every 5 minutes
- [ ] Dashboard displays current + historical data
- [ ] API response time <500ms for all endpoints
- [ ] All code committed with clear messages
- [ ] Documentation up-to-date and complete
