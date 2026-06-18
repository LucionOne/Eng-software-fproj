# Strategy & Design Rationale

## Project Scope
Build a lightweight garden monitoring system in under one week. Focus: well-designed, maintainable code over feature completeness.

## Key Decisions

### Language: Python ✓
- **Why:** Rapid prototyping, simple syntax, excellent for small projects
- **Status:** Chosen and actively used

### Framework: FastAPI ✓
- **Why:** Modern, type-safe, minimal boilerplate, auto-generated docs
- **Status:** Running on port 3002; serves dashboard and API endpoints

### Database: SQLite ✓
- **Why:** Zero external dependencies, file-based, sufficient for single-instance local use
- **Status:** Active; integrated with DatabaseManager class

### Architecture: Threading + Input Validation ✓
- **Why:** Simpler initial implementation, easier debugging; validation prevents data corruption
- **Current:** DataPuller uses threading for continuous ingestion with sensor value & datetime validation
- **Future:** Refactor to async/await if scaling to multiple ingestion sources

### Frontend: Static HTML/JS ✓
- **Why:** One less service to maintain; FastAPI serves static files natively
- **Status:** dashboard.html implemented; served at root endpoint

## Validation Boundary
Data ingestion now enforces:
- **Temperature:** -50°C to 60°C (physically plausible)
- **Humidity:** 0–100%
- **pH:** 0–14
- **DateTime:** ISO 8601 format required
- **Logging:** Invalid readings logged but never persisted (prevents data corruption)

## Quality Standards
- **Code:** Small, well-named functions; self-documenting where possible
- **Testing:** Unit tests for critical components (DatabaseManager, DataPuller)
- **Documentation:** This suite of markdown files captures all decisions
- **Commits:** Atomic, clear messages with references to objectives

## Risk Mitigation
1. **Hardware unavailable:** Mitigated by mock API simulator
2. **Scope creep:** Fixed 1-week timeline; features drop after that
3. **Database issues:** Tested DatabaseManager early to catch issues
4. **Integration failures:** Staged development (manager → API → dashboard)