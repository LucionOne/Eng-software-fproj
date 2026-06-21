# Stakeholder Analysis – Garden Manager MVP

## 1. Stakeholder Identification

### Primary Stakeholders

| Stakeholder | Role | Interests | Impact | Influence |
|---|---|---|---|---|
| **End User (Gardener)** | System operator | Real-time monitoring, ease of use, reliable data, offline access | High | High |
| **Product Owner / Team Lead (Guilherme P. Santos)** | Project decision-maker | On-time delivery, code quality, maintainability, scalability foundation | High | High |
| **Development Team** | Implementation | Clear requirements, reasonable scope, quality tooling | Medium | Medium |

### Secondary Stakeholders

| Stakeholder | Role | Interests | Impact | Influence |
|---|---|---|---|---|
| **Future IoT Hardware Provider** (v0.2) | Upstream integration partner | Stable data API contract, known data format, resilience | Medium | Low |
| **Dashboard Consumer (Future)** | Downstream system | Reliable HTTP API, consistent schema, performance SLA | Medium | Low |
| **System Administrator** (if deployed) | Operational | Easy deployment, logging, monitoring, troubleshooting | Low | Medium |

---

## 2. User Journey & Use Case Mapping

### Gardener Workflow (End User)

1. **Morning Check** → Opens dashboard at `http://localhost:3002` → Sees current temperature, humidity, pH
   - **Related UC:** UC-01 (Monitor Current Sensor Data)

2. **Daily Decision** → Reviews historical readings from the past 24 hours → Decides whether to water or adjust temperature
   - **Related UC:** UC-02 (Retrieve Historical Sensor Data)

3. **System Resilience** → Notices API is down → Dashboard shows stale data + "Retrying..." message → Refreshes page after 30 seconds and data is back
   - **Related UC:** UC-01 Exception 3a (API unreachable; graceful degradation)

4. **Data Trust** → System rejects a sensor reading with impossible temperature (155°C) → Logs show rejection but database remains clean
   - **Related UC:** UC-03 (Handle and Log Invalid Sensor Input)

---

## 3. Stakeholder Communication Plan

| Stakeholder | Communication Method | Frequency | Content |
|---|---|---|---|
| **End User** | Dashboard + error messages | Real-time | Current readings, last-update timestamp, error/retry status |
| **Product Owner** | Architecture docs, test results, commit messages | Daily/Weekly | SRS compliance, test coverage, risk status, blockers |
| **Development Team** | Code comments, process docs (docs/other/Process.md), PR reviews | Daily | DoR/DoD clarity, branching rules (docs/scm-plan.md), test requirements |
| **Future IoT Partner** | API contract docs (RFC + test evidence) | Pre-integration (v0.2) | Endpoint schema, timeout behavior, validation rules |

---

## 4. Acceptance & Validation

**v0.1 MVP Acceptance:**

- ✅ Dashboard displays current readings with last-update timestamp (UC-01)
- ✅ Dashboard incremental polling via `GET /data?after_id=N` reduces payload (UC-02)
- ✅ Invalid sensor readings logged but never persisted (UC-03)
- ✅ All unit tests pass: `python -m pytest tests/ -v` (docs/NEXT_STEPS.md Phase 4.1)
- ✅ No magic in error handling; all exceptions logged with context

**Success Metrics:**

| Metric | Target | Actual (v0.1) | Acceptable |
|---|---|---|---|
| API response time (<500ms) | GET /data <500ms | [TODO: benchmark] | ✓ if met |
| DataPuller uptime | >99% over 24h | [TODO: stress test] | ✓ if met |
| Data integrity (no corruption) | 100% valid readings only | [TODO: full audit] | ✓ if met |
| Test coverage (boundary validation) | ≥80% for DataPuller | tests/test_translate_from_api.py covers main paths | ✓ (partial) |

---

*This stakeholder analysis is derived from project scope (docs/README.md, docs/Strategy.md, docs/requirements/srs.md) and architecture decisions (RFC-001). It establishes shared understanding of who benefits from the system and what success looks like.*
