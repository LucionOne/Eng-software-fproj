| **Team** | **Version** | **Date** | **RFC reference** | **Associated milestone** |
|---|---:|---|---|---|
| Guilherme P. Santos (209635) | v0.1 | 2026-06-21 | [docs\rfc\rfc-001-arquitetura-mvp.md] | Marco 3 do PI |

## 1.1 Cabeçalho

## 1.2 Escopo desta estratégia

**What v0.1 covers:**

- Data ingestion and boundary validation via the existing `DataPuller` component (threaded ingestion, input validation as described in docs/Strategy.md).
- Storage and query surface provided by `DatabaseManager` (SQLite-based persistence; referenced in docs/architecture/architectureOfAll.md).
- API surface for reading data: root dashboard (`GET /`) and data export endpoint (`GET /data` and `GET /data?after_id=N`) as implemented in `src\classes\APIService.py` and documented in README.md.

**What is out of scope for v0.1 (moved to v0.2 / Marco 4):**

- Full, production-quality API routes listed in docs/NEXT_STEPS.md (e.g., `/api/sensors/current`, date-range queries) are not implemented and will be delivered in v0.2.
- Mock API server configuration and realistic sensor endpoint definitions (Phase 1.2 in docs/NEXT_STEPS.md).
- Comprehensive integration and acceptance testing (Phase 4 in docs/NEXT_STEPS.md) including end-to-end flows between Mock API → DataPuller → Database → API → Dashboard.

## 1.3 Matriz risco → teste

| UC | Risco técnico concreto | Nível de teste | Justificativa (1 frase) |
|----|------------------------|----------------|-------------------------|
| [TODO: UC ID from A1.3] | Missing database index on `sensor_logs` (queries by time range can degrade to full table scans) | integration | Index-related performance issues require integration tests exercising realistic data volumes and query patterns (see docs/architecture/architectureOfAll.md future considerations). |
| [TODO: UC ID from A1.3] | Threaded DataPuller may lose data or behave unpredictably on network timeouts or exceptions | system | Concurrency and external network dependencies necessitate system-level tests and fault-injection to validate resilience (see docs/Strategy.md and docs/NEXT_STEPS.md tasks). |
| [TODO: UC ID from A1.3] | API route duplication/definition ambiguity (duplicate `@app.get("/data")` handlers in `src\classes\APIService.py`) may cause undefined behavior | integration | Route-level integration tests will detect ambiguous routing and ensure correct status codes and payloads. |
| [TODO: UC ID from A1.3] | Invalid or malformed sensor payloads arriving from upstream (missing datetime, non-numeric values) can corrupt processing | unit/integration | Unit tests cover validation logic (see tests/test_translate_from_api.py), but integration tests are required to validate end-to-end handling when receiving malformed upstream data. |
| [TODO: UC ID from A1.3] | Lack of a mock API server makes end-to-end verification brittle and hard to reproduce | system | System tests with a controlled mock API are needed to reproduce real-world timing and data patterns as described in docs/NEXT_STEPS.md. |

## 1.4 Níveis de teste aplicados ao projeto

**unit**

Unit tests are implemented under `tests/` (e.g., `tests/test_translate_from_api.py`) and validate boundary logic inside `DataPuller` and other classes; they run locally with `python -m pytest tests/ -v` (docs/NEXT_STEPS.md provides the test command). Example: `DataPuller._translate_from_api` unit tests.

**integration**

Integration tests will exercise interactions between `DataPuller`, `DatabaseManager`, and `APIService` (for example: DataPuller writes rows to SQLite and APIService returns those rows via `GET /data`). These are not yet implemented; see Phase 4 in docs/NEXT_STEPS.md.

**system**

System tests simulate the full stack (Mock API → DataPuller → Database → API → Dashboard) to validate end-to-end behavior under realistic conditions and failure modes (network timeouts, large data volumes). NEXT_STEPS lists these as required e2e tests.

**acceptance**

Acceptance testing is deferred for v0.1 because the API layer and the mock API are incomplete (see docs/NEXT_STEPS.md). Acceptance tests will be appropriate once `/api/sensors/current` and dashboard flows are implemented in v0.2.

## 1.5 Técnica "moderna por contexto" escolhida — ADR

**Context:** the project requires a reliable API surface and repeatable verification of API contracts while the API layer and mock API are still under development (docs/NEXT_STEPS.md, docs/architecture/architectureOfAll.md).

**Decision:** adopt **contract testing** between the API provider (manager) and its consumers (dashboard and mock API). Implement provider-side contract tests that assert HTTP status codes, required JSON fields, and JSON schema for endpoints such as `GET /data` and planned `/api/sensors/current`.

**Alternatives rejected:**
- Full end-to-end-only testing: rejected because it requires a stable mock API and full integration to be in place for every test run (slower, brittle).

**Consequences:**
- Gains: faster, focused verification of API surface; clear contract for frontend and downstream components; easier CI gating.
- Costs: investment to define schemas and maintain contracts; initial work to extract precise response shapes from existing handlers.

**When not to use:**
- If the API surface becomes highly dynamic with frequent incompatible changes, contract testing should be complemented with broader integration tests; revisit decision in v0.2.

## 1.6 Estratégia de regressão

- **PR policy (required):** all unit tests under `tests/` must pass locally; repository currently provides `python -m pytest tests/ -v` as the test command (docs/NEXT_STEPS.md). **[TODO: configure CI pipeline to run this on every PR]**
- **Blocking vs non-blocking:** Unit test suite should block merges (policy to be enforced in CI). Integration and system tests are planned to run in scheduled jobs or gated for release candidates (see Phase 4 in docs/NEXT_STEPS.md). **[TODO: add CI jobs and explicit gating rules]**
- **Detecting regressions:** failures are detected via automated test runs (unit tests on PRs; integration/nightly); additionally, add test coverage reporting and nightly smoke runs against a pinned mock API instance. **[TODO: implement mock API and CI jobs]**

## 1.7 Evidência executável

**Provider-side contract test for `GET /data` endpoint:**

- **Test file:** `tests/test_contract_api_data.py` — 8 contract tests validating HTTP 200, JSON schema, required fields (id, recorded_at, temperature, humidity, ph), type consistency, and incremental query support (after_id parameter)
- **Execution log:** `docs/test-strategy/evidencias/pytest-contract-tests-20260621.log` — shows 8 PASSED tests (100% pass rate, 0.71s execution time)
- **Command to verify:** `python -m pytest tests/test_contract_api_data.py -v`

**Summary of evidence:**
- ✅ Validates HTTP 200 status code for `GET /data`
- ✅ Asserts JSON schema includes top-level `status: "ok"` and `data` object
- ✅ Confirms `data` contains `readings[]`, `latest_id`, `count` per RFC-001 Section 5.2
- ✅ Verifies each reading includes required fields matching SQL_config.py schema (id, recorded_at, temperature, humidity, ph)
- ✅ Type checks all fields (id: int, recorded_at: string, sensor values: float/int/null)
- ✅ Tests incremental query contract: `GET /data?after_id=N` returns same structure
- ✅ Confirms data consistency: count matches readings array length, latest_id equals max reading ID

**Directive A1-6 Section 1.7 compliance:** ✅ Minimum for v0.1 met — 1 executable test running that validates a real contract (schema + status code + required field) for the `GET /data` endpoint.

## 1.8 Próximos passos (o que vai para v0.2)

- Implement full API routes and `/api/sensors/current` and date-range queries (docs/NEXT_STEPS.md Phase 2) — required before acceptance tests.
- Provide a reproducible Mock API server and seed data for system tests (docs/NEXT_STEPS.md Phase 1.2).
- Add provider contract tests for API endpoints and CI gating for unit and contract suites.
- Implement integration and end-to-end tests (Phase 4) and add database indexing for performance (docs/architecture/architectureOfAll.md future considerations).

---