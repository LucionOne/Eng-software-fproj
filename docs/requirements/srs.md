# Software Requirements Specification (SRS)
**Garden Manager MVP**

---

## Use Cases

### UC-01: Monitor Current Sensor Data in Dashboard

**Actor Principal:** End User (via web dashboard)

**Pre-conditions:**
- The Manager service is running and listening on `http://localhost:3002`
- The Mock API is active and feeding sensor data to DataPuller
- At least one sensor reading exists in the SQLite database

**Fluxo Principal:**
1. User navigates to `http://localhost:3002` in a web browser
2. Dashboard loads `src/assets/dashboard.html`
3. JavaScript on the dashboard makes `GET /data` request to the Manager API
4. Manager's `get_data()` endpoint fetches all rows from `sensor_logs` table
5. API returns JSON response with status `"ok"`, a list of readings (each with `id`, `temperature`, `humidity`, `ph`, timestamp), `latest_id`, and `count`
6. Dashboard renders the latest readings (temperature, humidity, pH) with units
7. Dashboard displays timestamp of last update and total record count

**Fluxos Alternativos:**
- **1a. First load (empty database):** If no readings exist, API returns empty `readings[]`, `latest_id: null`, and `count: 0`. Dashboard displays "No data yet; waiting for sensor readings."

**Fluxos de Exceção:**
- **3a. API unreachable:** If `GET /data` returns HTTP 500 or connection timeout (>5 seconds), dashboard displays error message "Connection lost. Retrying in 30 seconds..." and auto-retries every 30 seconds.
- **4a. Database query error:** If DatabaseManager encounters SQLite error (e.g., locked database), `get_data()` logs the error and returns HTTP 500 with message `{"status": "error", "message": "Database unavailable"}`. Dashboard treats this as unreachable (see 3a).
- **5a. Malformed JSON response:** If API returns unparseable JSON, browser console logs error and dashboard shows generic error banner.

**Pós-condições (success):**
- Dashboard displays current sensor readings with a visible timestamp showing when data was last fetched.

**Pós-condições (failure):**
- Dashboard shows user-facing error message; user can manually refresh or wait for auto-retry.

---

### UC-02: Retrieve Historical Sensor Data for Incremental Updates

**Actor Principal:** Dashboard JavaScript (polling for new data)

**Pre-conditions:**
- Manager service is running
- At least one sensor reading exists in the database
- Dashboard has successfully loaded and has recorded the last `id` from a prior `GET /data` call (e.g., `latest_id = 100`)

**Fluxo Principal:**
1. Dashboard timer triggers every 30 seconds
2. JavaScript calls `GET /data?after_id=100` to fetch only new readings added since the last known ID
3. Manager's `get_data_since(after_id)` handler executes `SELECT * FROM sensor_logs WHERE id > ? ORDER BY id ASC`
4. API calculates new `count` (number of rows returned) and `latest_id` from the result set
5. API returns JSON with all new readings, new count, and updated `latest_id`
6. Dashboard appends new readings to its in-memory history and updates displayed timestamp
7. Dashboard updates `latest_id` for the next poll

**Fluxos Alternativos:**
- **2a. No new data:** If no rows exist with `id > after_id`, API returns `readings: []`, `count: 0`, `latest_id: null`. Dashboard skips UI update and polls again in 30 seconds.

**Fluxos de Exceção:**
- **3a. Invalid after_id parameter:** If `after_id` parameter is malformed (e.g., non-integer), the parameter binding fails or is ignored. Query either executes with `after_id = 0` (default) or returns 400 Bad Request. **[TODO: clarify integer validation in APIService.py]**
- **4a. Database query returns no results but error occurred silently:** If SQLite query fails (e.g., sensor_logs table was dropped), DatabaseManager logs the error and returns HTTP 500. Dashboard treats as unreachable (see UC-01 exception 3a).
- **5a. Network loss mid-request:** Request timeout (>5 seconds); dashboard logs warning and retries on next cycle (no data lost; next poll will fetch all data since last successful poll).

**Pós-condições (success):**
- Dashboard history is updated with new sensor readings; `latest_id` is incremented and ready for next poll.

**Pós-condições (failure):**
- Dashboard retains last known `latest_id` and retries on next cycle; no data is double-counted or lost.

---

### UC-03: Handle and Log Invalid Sensor Input from Upstream Mock API

**Actor Principal:** DataPuller (threaded data ingestion component)

**Pre-conditions:**
- Manager service is running
- DataPuller thread is active and calling the Mock API at regular intervals
- Mock API returns a JSON payload with sensor data

**Fluxo Principal:**
1. DataPuller polls Mock API endpoint for current sensor readings (e.g., `GET http://localhost:5000/api/sensors/current` or similar, per docs/NEXT_STEPS.md Phase 1.2)
2. Mock API returns JSON payload with fields: `datetime`, `sensors` (array of objects with `sensor_type` and `value`)
3. DataPuller calls `DataPuller._translate_from_api(payload)` to validate and extract fields
4. `_translate_from_api` performs boundary validation:
   - Datetime must be ISO 8601 format (e.g., `"2024-01-15T10:30:00+00:00"`); rejects invalid format
   - Temperature must be in range [-50°C, 150°C]; out-of-range values are skipped
   - Humidity must be in range [0%, 100%]; out-of-range values are skipped
   - pH must be in range [0, 14]; out-of-range values are skipped
   - Non-numeric sensor values are skipped (e.g., `"value": "N/A"` or `null`)
5. Valid readings are accumulated into a tuple `(datetime, temperature, humidity, ph)` (with `None` for missing/invalid sensors)
6. Tuple is passed to DatabaseManager for persistence to `sensor_logs` table
7. Invalid readings are logged to `src/lib/logger.py` with details (which field, which value, why rejected)

**Fluxos Alternativos:**
- **2a. Mock API returns partial data:** If payload contains only temperature and humidity (no pH), the tuple is `(datetime, temp, humid, None)` and is persisted as-is.
- **3a. Datetime is Z timezone:** If datetime is `"2024-01-15T10:30:00Z"`, `_translate_from_api` normalizes it to `"2024-01-15T10:30:00+00:00"` before returning.

**Fluxos de Exceção:**
- **1a. Network timeout:** If Mock API does not respond within N seconds (timeout configurable in DataPuller), request fails gracefully. Thread logs warning and retries on next interval (e.g., 5 minutes later). No exception is raised to caller.
- **2a. Mock API returns invalid JSON:** Response body is not valid JSON. DataPuller logs `ValueError` with the raw response and skips this polling cycle.
- **3a. Missing required fields:** If payload is missing `datetime` or `sensors` key, `_translate_from_api` raises `TypeError` or `ValueError` with specific message (e.g., `"datetime must be a string"`). DataPuller catches exception, logs it, and continues (does not persist anything for this cycle).
- **4a. All sensors invalid for one reading:** If all sensor values in a payload are out-of-range or non-numeric, `_translate_from_api` raises `ValueError` with message `"no valid sensor measurements found"`. DataPuller logs this and skips the reading (no partial record persisted).
- **5a. Database write fails:** If DatabaseManager.insert_reading() encounters SQLite error (e.g., locked database, primary key violation), DataPuller logs the error and retries on next cycle. The invalid reading is NOT persisted; no data corruption occurs.

**Pós-condições (success):**
- Valid reading is persisted to `sensor_logs`; invalid fields are logged but never written to database (maintains data integrity per docs/Strategy.md validation boundary).

**Pós-condições (failure):**
- Invalid reading is logged with full context; database remains unmodified. DataPuller continues to next polling cycle; no exception propagates to user.

---

## Functional Requirements

| ID | Description | Priority | Acceptance Criterion |
|----|---|---|---|
| FR-01 | System MUST accept sensor data from Mock API in JSON format with fields: `datetime`, `sensors` array | MUST | Request to `GET /api/sensors/current` (or configured endpoint) returns valid JSON within 2 seconds; payload can be deserialized by `json.loads()` |
| FR-02 | System MUST validate datetime in ISO 8601 format and normalize Z timezone to +00:00 | MUST | Test case: `"2024-01-15T10:30:00Z"` becomes `"2024-01-15T10:30:00+00:00"`; test case: `"invalid"` raises `ValueError` |
| FR-03 | System MUST reject temperature readings outside [-50°C, 150°C] without corrupting database | MUST | Test: payload with `temp = -51.0` is skipped; payload with `temp = 150.0` is accepted; no partial record written |
| FR-04 | System MUST reject humidity readings outside [0%, 100%] without corruption | MUST | Test: payload with `humidity = 101.0` is skipped; valid readings in same payload are persisted |
| FR-05 | System MUST reject pH readings outside [0, 14] without corruption | MUST | Test: payload with `pH = 14.1` is skipped; valid readings persisted |
| FR-06 | System MUST provide `GET /data` endpoint returning all sensor logs with status, readings array, latest_id, and count | MUST | Endpoint returns HTTP 200; response body matches schema `{"status": "ok", "data": {"readings": [...], "latest_id": N, "count": N}}`; fields are present in every call |
| FR-07 | System MUST provide `GET /data?after_id=N` endpoint returning only readings with `id > N` | MUST | Test: database has IDs 1-100; `GET /data?after_id=50` returns only IDs 51-100; test: `GET /data?after_id=999` returns empty array |
| FR-08 | System MUST serve dashboard HTML at `GET /` with content-type `text/html` | MUST | Request to `/` returns HTTP 200 and HTML content (not JSON); dashboard renders in browser without errors |
| FR-09 | System MUST log invalid/rejected sensor readings with context (field name, value, reason) | SHOULD | Log entries contain timestamp, field name (e.g., "temperature"), rejected value, and reason (e.g., "out of range [-50, 150]") |

## Non-Functional Requirements (FURPS+)

| ID | Category | Description | Metric / Acceptance Criterion |
|----|---|---|---|
| NFR-01 | **Performance** | API endpoint response time MUST be acceptable for dashboard polling | `GET /data` with <100 readings returns in <500ms; `GET /data?after_id=N` returns in <200ms (99th percentile) |
| NFR-02 | **Performance** | DataPuller MUST poll Mock API and persist valid data without blocking other requests | Thread does not consume >10% CPU while idle; ingestion latency (poll → persist) <3 seconds for single reading |
| NFR-03 | **Scalability** | System MUST maintain performance with up to 100k sensor readings in database | Database query time <500ms at 100k rows; no sequential full table scans for time-based queries (indexes TBD in v0.2) |
| NFR-04 | **Reliability** | DataPuller MUST gracefully recover from network timeouts | If Mock API is unreachable, DataPuller retries after N seconds (configurable, default 5 min); no exception crashes the thread |
| NFR-05 | **Reliability** | System MUST guarantee no data corruption on database write failures | If `INSERT INTO sensor_logs` fails, transaction is rolled back; no partial records written; no exceptions propagate to user |
| NFR-06 | **Data Integrity** | Invalid sensor readings MUST NEVER be persisted | 100% of invalid readings (out-of-range, malformed) are rejected before `INSERT`; confirmed by test coverage in `tests/test_translate_from_api.py` |
| NFR-07 | **Usability** | Dashboard MUST provide visual feedback when data is stale or API is unreachable | Dashboard displays error message within 10 seconds of API failure; auto-retry indicator shown to user |
| NFR-08 | **Maintainability** | Code MUST be logged at boundaries (data ingestion, API, database errors) | Every exception in DataPuller, APIService, and DatabaseManager is caught and logged with context (not silently ignored) |
| NFR-09 | **Deployment** | System MUST run on Python 3.8+ with FastAPI and SQLite3 | Minimum versions: Python 3.8, FastAPI 0.95+, SQLite 3.22+; no external database server required |
| NFR-10 | **Testing** | Unit test coverage MUST include boundary validation and error cases | Test suite includes tests for all rejection criteria (temp out of range, invalid datetime, etc.); minimum 80% branch coverage for DataPuller and DatabaseManager |

---

