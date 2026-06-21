# RFC-001: Garden Manager MVP Architecture

## Header

| Attribute | Value |
|---|---|
| **Status** | Accepted (v0.1 MVP) |
| **Version** | 1.0 |
| **Author(s)** | Guilherme P. Santos (209635) |
| **Date** | 2026-06-21 |
| **Associated Milestone** | Marco 3 do PI (v0.1 MVP) |
| **RFC ID** | RFC-001 |

---

## 1. Context and Business Motivation

**Problem:** Home gardeners and small-scale farmers lack a unified, low-cost system to monitor environmental conditions (temperature, humidity, soil pH) in real-time and retain historical data for analysis. Most commercial solutions require external APIs, subscription services, or complex hardware setup.

**Solution:** Build a lightweight, self-hosted garden monitoring system that aggregates sensor data (via mock API in v0.1; real IoT sensors in v1.0), persists readings to a local database, and exposes a web-based dashboard for real-time and historical analytics. The system prioritizes simplicity, maintainability, and robustness in the face of network instability.

**Business Goals:**
- Enable gardeners to make data-informed decisions about watering, temperature control, and soil management.
- Eliminate dependency on external SaaS platforms; data remains on-premises.
- Provide a foundation for future features (alerts, automations, integration with smart irrigation hardware).

---

## 2. Scope of This Milestone (v0.1)

### In Scope (v0.1)

- **Data Ingestion:** Mock API endpoint simulating realistic sensor data (temperature, humidity, pH) with ISO 8601 timestamps.
- **Validation Boundary:** Strict input validation on all sensor readings before persistence; rejection of out-of-range values (temperature -50…150°C, humidity 0…100%, pH 0…14) without database corruption.
- **Storage:** SQLite-based sensor_logs table persisting validated readings with auto-incrementing ID, timestamp, and three numeric fields (temperature, humidity, pH).
- **API Surface:** Two FastAPI endpoints:
  - `GET /data` — fetch all readings (for UC-01: Monitor Sensor Data)
  - `GET /data?after_id=N` — fetch readings since last known ID (for UC-02: Incremental Updates)
- **Dashboard:** Static HTML/JavaScript single-page application served at `GET /` (root endpoint), displaying current readings and last-update timestamp.
- **Error Handling:** Graceful degradation when Mock API is unreachable; retries with exponential backoff; clear logging of all validation failures.

### Out of Scope (v0.2 / Marco 4)

- **Real IoT Hardware:** Mock API will be replaced with real ESP32 sensors and proper MQTT or HTTP bridge in v0.2.
- **Advanced API Routes:** Date-range queries (`GET /api/data?from=X&to=Y`), filtering by metric, and complex analytics endpoints are deferred to Phase 2 (docs/NEXT_STEPS.md).
- **UI Enhancements:** Historical charts, exportable reports, and multi-site dashboards planned for v0.2.
- **Authentication & Authorization:** No user login or role-based access control in v0.1; assumed single-user, local-network deployment.
- **Horizontal Scaling:** No clustering, caching, or database replication; single-instance SQLite only.

---

## 3. Requirements Addressed

### Referenced SRS (docs/requirements/srs.md)

**Critical Use Cases Implemented:**

- **UC-01: Monitor Current Sensor Data in Dashboard** — Dashboard calls `GET /data` to display live readings; fulfilled by APIService.get_data() and dashboard.html polling loop.
- **UC-02: Retrieve Historical Sensor Data for Incremental Updates** — Dashboard incremental polling via `GET /data?after_id=N`; fulfilled by APIService.get_data_since() and client-side state tracking.
- **UC-03: Handle and Log Invalid Sensor Input** — DataPuller._translate_from_api() validates all upstream payloads; invalid readings logged and never persisted; fulfilled by src/classes/dataPuller.py boundary validation.

**Functional Requirements:**

- FR-01 through FR-09: Data format, validation, endpoint contracts, dashboard serving, and logging. All addressed by components described in Section 6 (Architecture).

**Non-Functional Requirements:**

- NFR-01 (Performance): `GET /data` target <500ms; achieved via lightweight FastAPI framework and SQLite queries (optimization planned for v0.2 with indexes).
- NFR-02 (Threading): DataPuller runs in dedicated thread; <10% CPU while idle.
- NFR-04 (Reliability): Network timeouts handled gracefully (retries, no crashes).
- NFR-05 (Data Integrity): Validation boundary ensures no partial or corrupted records.
- NFR-06 (Testing): Unit tests in tests/test_translate_from_api.py cover all rejection criteria.

---

## 4. Technology Stack

| Component | Technology | Version | Rationale |
|---|---|---|---|
| **Language** | Python | 3.8+ | Rapid iteration; excellent libraries for data processing and web services; suitable for small team, tight timeline |
| **Web Framework** | FastAPI | 0.95.0 | Minimal boilerplate; type hints enable auto-generated OpenAPI docs; async-ready if refactored in future; fast JSON serialization |
| **Database** | SQLite | 3.22+ | Zero external dependencies; file-based (no server); sufficient for single-instance, local-network deployment; sufficient for 100k+ records (with indexing in v0.2) |
| **HTTP Client** | requests | 2.28.0 | Standard Python HTTP library; simple, well-documented; used by DataPuller to poll Mock API |
| **Concurrency** | Python threading | stdlib | Lightweight; simpler than asyncio for v0.1 (no async complexity); can refactor to asyncio in v0.2 if needed |
| **Frontend** | HTML5 + Vanilla JS | ES6 | No external build step; served directly by FastAPI; no npm/webpack overhead; sufficient for data-display SPA |
| **Logging** | Python logging | stdlib | Built-in; no external dependency; structured logging planned for v0.2 |
| **Testing** | pytest | 7.0+ | Standard Python test runner; fixtures, assertions, and plugin ecosystem |

---

## 5. System Architecture

### 5.1 Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   Browser / Dashboard                   │
│  (HTML5 + JS: fetch, DOM manipulation, polling loop)    │
└─────────────────────────┬───────────────────────────────┘
                          │ HTTP: GET /data, GET /data?after_id=N
                          ▼
┌──────────────────────────────────────────────────────────┐
│                   FastAPI Manager (Port 3002)            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  APIService (src/classes/APIService.py):                 │
│    @app.get("/")            → Dashboard HTML             │
│    @app.get("/data")        → get_data() handler         │
│    @app.get("/data?after_id=N") → get_data_since()       │
│                                                          │
│  Routes ↕ DatabaseManager (sqlite query wrapper)         │
│                                                          │
│  DatabaseManager ↕ SQLite Database                       │
│                  (sensor_logs table)                     │
│                                                          │
│  DataPuller (separate thread):                           │
│    - Polls Mock API every N seconds                      │
│    - Validates input via _translate_from_api()           │
│    - Calls db.insert_reading() for valid data            │
│    - Logs invalid readings without persisting            │
│                                                          │
└──────────────────────────┬───────────────────────────────┘
                           │ HTTP: GET /api/sensors/current (v0.1)
                           │ (will become MQTT in v0.2)
                           ▼
                 ┌─────────────────────────┐
                 │   Mock API              │
                 │ (mock/mock_main.py)     │
                 │ Simulates sensor data   │
                 │ temp, humidity, pH      │
                 └─────────────────────────┘
```

### 5.2 Data Flow Scenario 1: Dashboard displays current reading (UC-01)

```
1. User navigates to http://localhost:3002 in browser
2. Browser receives dashboard.html from APIService.get_html()
3. JavaScript executes on page load:
   - fetch('GET /data')
4. APIService routes to get_data()
5. get_data() calls db.fetch_data("SELECT * FROM sensor_logs")
6. DatabaseManager executes query, returns list of rows
7. get_data() builds JSON response:
   {
     "status": "ok",
     "data": {
       "readings": [
         {"id": 1, "timestamp": "...", "temperature": 23.5, "humidity": 60, "ph": 7.1},
         ...
       ],
       "latest_id": N,
       "count": N
     }
   }
8. Browser receives JSON; JavaScript updates DOM:
   - Displays: Temperature 23.5°C, Humidity 60%, pH 7.1
   - Displays: Last updated 2024-06-21 10:30:00 UTC
```

### 5.3 Data Flow Scenario 2: DataPuller ingests and validates sensor data (UC-03)

```
1. DataPuller thread wakes up (every 5 minutes by default)
2. Makes HTTP GET request to Mock API:
   GET http://localhost:5000/api/sensors/current
3. Mock API responds with JSON:
   {
     "datetime": "2024-06-21T10:30:00+00:00",
     "sensors": [
       {"sensor_type": "Temperature", "value": 23.5},
       {"sensor_type": "Humidity", "value": 60.0},
       {"sensor_type": "Ph", "value": 7.1}
     ]
   }
4. DataPuller calls _translate_from_api(payload)
5. _translate_from_api() validates:
   - Datetime: ISO 8601 format ✓
   - Temperature: -50 to 150°C ✓ (23.5 passes)
   - Humidity: 0 to 100% ✓ (60 passes)
   - pH: 0 to 14 ✓ (7.1 passes)
6. Returns tuple: ("2024-06-21T10:30:00+00:00", 23.5, 60.0, 7.1)
7. DataPuller calls db.insert_reading(datetime, temp, humid, ph)
8. DatabaseManager inserts row into sensor_logs:
   INSERT INTO sensor_logs (timestamp, temperature, humidity, ph)
   VALUES ("2024-06-21T10:30:00+00:00", 23.5, 60.0, 7.1)
9. Row committed; available for next GET /data query
```

### 5.4 Boundary Responsibilities

| Boundary | Responsibility |
|---|---|
| **DataPuller ↔ Mock API** | DataPuller is the consumer; Mock API is the provider. DataPuller must handle: timeouts, malformed JSON, missing fields, out-of-range values. |
| **DataPuller ↔ DatabaseManager** | DataPuller is the writer; DatabaseManager is the persistence layer. Contract: _translate_from_api() guarantees valid tuples only; insert_reading() must not raise on transient failures (retry). |
| **APIService ↔ DatabaseManager** | APIService is the reader; DatabaseManager executes queries. Contract: fetch_data() returns rows as dicts; API serializes to JSON. |
| **APIService ↔ Browser** | APIService returns JSON; Browser deserializes and renders. Contract: Response schema is stable (see Functional Requirement FR-06). |
| **DataPuller ↔ Logger** | All exceptions and invalid readings logged with full context; logger never raises. |

---

## 6. Architecture Decisions (ADRs)

### ADR-001: Input Validation at Boundary (DataPuller) Rather Than in Database

**Context:**
- Sensor data arrives from untrusted upstream (Mock API, later real IoT devices).
- Invalid readings (out-of-range values, malformed datetimes) can corrupt analytics and user trust.
- Options: (a) validate before persistence, (b) store as-is and filter on read, (c) store with metadata flag.

**Decision:**
Implement **strict validation in DataPuller._translate_from_api()** before any call to DatabaseManager.insert_reading(). Invalid readings are logged but never persisted.

**Rationale:**
- **Maintains data integrity:** Database contains only valid, usable readings; no need for queries to filter garbage.
- **Simplifies debugging:** Clear separation of concerns; validation logic centralized in one place.
- **Supports compliance:** Logging of rejected readings provides audit trail for quality assurance.
- **Reduces storage:** Invalid data never written; saves I/O and storage overhead.

**Alternatives Rejected:**
- **(b) Store as-is, filter on read:** Would require every query to filter; complex WHERE clauses; risk of bugs leaking invalid data to users.
- **(c) Flag as valid/invalid:** Adds complexity to schema; still requires filtering on read; no real advantage.

**Consequences:**
- **Gain:** Simple, clean database; easier to reason about data quality.
- **Cost:** Validation logic must be comprehensive (all edge cases tested); rejected readings logged to separate stream (could become large log file in future; rotate in v0.2).

**When Not to Use:**
- If upstream data is already guaranteed valid (trusted source with contractual SLA); then defer validation to database layer for flexibility.
- If a regulatory requirement mandates retention of all upstream data (even invalid); then use option (c) with metadata flag.

---

### ADR-002: Lightweight Threading (Python threading module) Over async/await for v0.1

**Context:**
- System needs to poll Mock API in background while serving HTTP requests.
- Python concurrency options: threading, asyncio, multiprocessing, or external queue (Celery).
- Project has 1-week deadline; team is small; simplicity is paramount.

**Decision:**
Use Python's `threading` module in v0.1. DataPuller runs in a dedicated thread; DatabaseManager and APIService are thread-safe via SQLite connection pooling. Plan refactor to asyncio in v0.2 if scaling is needed.

**Rationale:**
- **Simplicity:** threading is easier to understand and debug than asyncio for beginners.
- **No external deps:** asyncio requires careful structuring of I/O; threading works with blocking I/O (requests library).
- **Sufficient for v0.1:** Single polling thread + single API thread is not a performance bottleneck.
- **Gradual migration:** Can refactor to asyncio later without changing external interfaces.

**Alternatives Rejected:**
- **asyncio:** Requires rewriting DataPuller with async I/O, async database access; steeper learning curve; premature optimization for v0.1.
- **multiprocessing:** Overkill for this workload; adds complexity with inter-process communication and database locking (SQLite is single-writer).
- **Celery (external queue):** Introduces external service dependency; not justified for single polling thread.

**Consequences:**
- **Gain:** Fast time-to-market; easy to debug thread issues; minimal code changes.
- **Cost:** GIL (Global Interpreter Lock) limits true parallelism; if CPU-bound processing emerges, must refactor; not suitable for 1000+ concurrent dashboard clients (but not a v0.1 requirement).

**When Not to Use:**
- If dashboard scales to >100 concurrent users and CPU profiling shows bottleneck in threading, refactor to asyncio.
- If DataPuller becomes CPU-intensive (complex transformations), consider separate process.
- If multiple independent polling threads are needed (v0.2 multi-source ingestion), migrate to asyncio to avoid thread coordination complexity.

---

## 7. Wireframes (UI Mockups)

### Screen 1: Dashboard – Current Readings (Responsive Layout)

```
┌─────────────────────────────────────────────────────────┐
│  🌱 Garden Manager Dashboard                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Current Readings (Updated: 2024-06-21 10:30:00 UTC)  v │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 🌡️  Temperature        23.5 °C                  │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 💧 Humidity           60.0 %                    │   │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ ⚗️  pH Level          7.1                      │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ Total Readings: 1,245                           │    │
│  │ Data Source: Active & Connected ✓               │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  [Manual Refresh]                                       │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ Scope: UC-01 (Monitor Current Sensor Data)              │
└─────────────────────────────────────────────────────────┘
```

**Related UC:** UC-01 (Monitor Current Sensor Data in Dashboard)

**Fulfillment:**
- Dashboard makes `GET /data` request to APIService.get_data()
- APIService returns all readings; browser renders latest as displayed above
- Timestamp is updated on each successful poll (every 30 seconds by default)

---

### Screen 2: Dashboard – Update History Indicator

```
┌─────────────────────────────────────────────────────────┐
│  🌱 Garden Manager Dashboard                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Current Readings (Updated: 2024-06-21 10:30:00 UTC)   │
│  [New: 3 readings since last update]                   │
│                                                         │
│  🌡️  Temperature        23.5 °C                         │
│  💧 Humidity           60.0 %                           │
│  ⚗️  pH Level          7.1                              │
│                                                         │
│  Last 5 readings (last 2.5 hours):                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │ ID  │ Time             │ Temp  │ Humid │ pH     │   │
│  │ 1243│ 10:30:00 +00:00 │ 23.5  │ 60.0  │ 7.1    │   │
│  │ 1242│ 10:00:00 +00:00 │ 23.2  │ 61.0  │ 7.0    │   │
│  │ 1241│ 09:30:00 +00:00 │ 23.0  │ 62.0  │ 7.1    │   │
│  │ ...  │ ...              │ ...   │ ...   │ ...    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ Scope: UC-02 (Incremental Updates via after_id)         │
└─────────────────────────────────────────────────────────┘
```

**Related UC:** UC-02 (Retrieve Historical Sensor Data for Incremental Updates)

**Fulfillment:**
- Dashboard stores last `latest_id` from previous `GET /data` call
- Subsequent polls use `GET /data?after_id=<last_id>` to fetch only new readings
- UI updates display with new data; history table appends rows

---

### Screen 3: Data Validation & Logging (Backend, not visible to user)

```
┌─────────────────────────────────────────────────────────┐
│  Logs: DataPuller Validation (Visible in Console)       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ [2024-06-21 10:30:05] INFO: Polling Mock API...         │
│ [2024-06-21 10:30:06] INFO: Valid reading received      │
│   datetime=2024-06-21T10:30:00+00:00                    │
│   temperature=23.5, humidity=60.0, ph=7.1               │
│   Row inserted: id=1243                                 │
│                                                         │
│ [2024-06-21 10:35:05] WARNING: Invalid sensor reading   │
│   Reason: temperature=155.0 out of range [-50, 150]     │
│   Reading rejected; not persisted                       │
│                                                         │
│ [2024-06-21 10:40:05] ERROR: Mock API timeout           │
│   Request to http://localhost:5000/ timed out (>5s)     │
│   Retrying in 5 minutes...                              │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ Scope: UC-03 (Handle and Log Invalid Sensor Input)      │
└─────────────────────────────────────────────────────────┘
```

**Related UC:** UC-03 (Handle and Log Invalid Sensor Input from Upstream Mock API)

**Fulfillment:**
- Logger in src/lib/logger.py records all validation outcomes (success, rejection, error)
- Logs include field name, value, and reason for rejection
- Logs are written to console and file (if configured); no exceptions escape to user

---

### Screen 4: Error State (API Unreachable)

```
┌─────────────────────────────────────────────────────────┐
│  🌱 Garden Manager Dashboard                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ⚠️  Connection Error                                   │
│                                                         │
│  The data server is unreachable. Last known data:       │
│                                                         │
│  Current Readings (as of 2024-06-21 10:00:00 UTC)       │
│  [Data is 30+ minutes stale]                            │
│                                                         │
│  🌡️  Temperature        23.2 °C                         │
│  💧 Humidity           61.0 %                           │
│  ⚗️  pH Level          7.0                              │
│                                                         │
│  Retrying in 30 seconds... ⏳                           │
│  [Retry Now]                                            │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ Scope: Exception handling in UC-01 (API unreachable)    │
└─────────────────────────────────────────────────────────┘
```

**Related UC:** UC-01 Exception 3a (API unreachable; dashboard displays error)

**Fulfillment:**
- When `GET /data` times out or returns 500, JavaScript catches error
- UI displays error message and last-known data
- Auto-retry timer begins; user can click "Retry Now" to force immediate retry

---

## 8. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| **Mock API is not reproducible** (v0.1 → v0.2 transition) | Medium | High | Implement Mock API with fixed seed data in mock/mock_main.py (already done). Document endpoint contracts. Plan real IoT integration tests for v0.2. | Guilherme |
| **Database query performance degrades at 100k+ rows** | Medium | High | Plan database indexing (CREATE INDEX on timestamp, sensor_id) for v0.2. Current design does not include indexes to minimize scope of v0.1. Monitor query times in logs. | Guilherme |
| **DataPuller thread crashes silently, data ingestion stops** | Low | High | Wrap DataPuller main loop in try/except that logs all exceptions and retries. Add health check endpoint (GET /health) in APIService to detect when DataPuller is unresponsive (planned v0.2). | Guilherme |
| **SQLite database locked during concurrent writes** | Low | Medium | SQLite has built-in serialization; queue writes to single thread via DatabaseManager. Test concurrent access under load (Phase 4, docs/NEXT_STEPS.md). | Guilherme |
| **Validation boundary is incomplete; invalid data leaks into database** | Medium | High | Comprehensive unit tests for _translate_from_api() covering all rejection criteria (temp, humidity, pH, datetime). Code review on validation logic before v0.1 release. | Guilherme |
| **Dashboard loses data on page refresh** (no persistence) | Low | Low | Expected behavior for v0.1 (stateless web app). Data persists on server (database); dashboard state is ephemeral. Document as known limitation. | Guilherme |

---

## 9. Out of Scope / Next Steps (v0.2)

**Features deferred to Marco 4 (v0.2):**

1. **Real IoT Hardware Integration**
   - Replace Mock API with real ESP32 sensor endpoints
   - Test MQTT broker integration or HTTP bridge
   - Update DataPuller to handle real-world latency and packet loss

2. **Advanced API Endpoints**
   - `GET /api/data?from=ISO&to=ISO` — date-range queries
   - `GET /api/data?metric=temperature` — filter by sensor type
   - Pagination support for large result sets

3. **Performance Optimization**
   - Add database indexes (timestamp, sensor_id)
   - Implement query caching for frequently-accessed time ranges
   - Profile and optimize SQLite queries for 100k+ row datasets

4. **UI Enhancements**
   - Historical charts (line graph, temperature trends over 24 hours)
   - Export functionality (CSV, JSON)
   - Alert thresholds (e.g., "notify if temperature exceeds 30°C")

5. **Infrastructure**
   - CI/CD pipeline with automated unit test and linting (Phase 5, docs/NEXT_STEPS.md)
   - Docker containerization for easier deployment
   - Health check and monitoring endpoints

6. **Acceptance Testing**
   - Full end-to-end tests (Mock API → DataPuller → Database → API → Dashboard)
   - Load testing with realistic data volumes

---

## 10. References

- **SRS:** docs/requirements/srs.md (defines UC-01, UC-02, UC-03 and functional/non-functional requirements)
- **Architecture Overview:** docs/architecture/architectureOfAll.md
- **Project Strategy:** docs/Strategy.md (validation boundaries, design decisions)
- **Development Process:** docs/other/Process.md (DoR, DoD, branching)
- **Next Steps:** docs/NEXT_STEPS.md (roadmap for v0.2)
- **Existing Tests:** tests/test_translate_from_api.py (validation logic coverage)

---
