# Strategy & Design Rationale

## Project Scope
Build a lightweight garden monitoring system in under one week. Focus: well-designed, maintainable code over feature completeness.

## Key Decisions

### Language: Python
- **Why:** Rapid prototyping, simple syntax, excellent for small projects
- **Concern:** No scaling required, so overhead is negligible

### Framework: FastAPI
- **Why:** Modern, type-safe, minimal boilerplate, auto-generated docs
- **Tradeoff:** Learning curve for async concepts, but threading suffices for MVP

### Database: SQLite
- **Why:** Zero external dependencies, file-based, sufficient for single-instance local use
- **Tradeoff:** Not suitable for distributed systems; acceptable here

### Architecture: Threading over Async
- **Why:** Simpler initial implementation, easier debugging
- **Future:** Refactor to async/await if scaling to multiple ingestion sources

### Frontend: Static HTML/JS
- **Why:** One less service to maintain; FastAPI serves static files natively
- **Tradeoff:** No dynamic template rendering; simple but sufficient

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