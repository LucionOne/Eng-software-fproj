## Contract Tests Evidence – v0.1 MVP

**Status:** ✅ **EXECUTABLE AND PASSING**

### Test File

- **Location:** `tests/test_contract_api_data.py`
- **Scope:** Provider-side contract tests for `GET /data` endpoint (RFC-001 ADR-001 boundary contract)

### Test Coverage

The contract test suite validates:

1. **HTTP Status:** `GET /data` returns HTTP 200 OK
2. **Content Type:** Response has `application/json` content-type
3. **Top-Level Schema:** Response includes required fields `status` and `data`
4. **Data Structure:** `data` object contains `readings` (list), `latest_id` (int or null), and `count` (int)
5. **Reading Fields:** Each reading includes `id`, `recorded_at`, `temperature`, `humidity`, `ph` (per SQL_config.py schema)
6. **Type Validation:** `id` is int, `recorded_at` is string (ISO 8601), sensor values are float/int/null
7. **Incremental Queries:** `GET /data?after_id=N` returns valid structure (UC-02 contract)
8. **Count Consistency:** `count` field matches actual readings array length
9. **Latest ID Accuracy:** `latest_id` equals max ID in readings, or null if empty

### Execution Log

- **File:** `docs/test-strategy/evidencias/pytest-contract-tests-20260621.log`
- **Result:** **8 passed, 1 warning** (warning is deprecation in httpx client, not a test failure)
- **Timestamp:** 2026-06-21 15:52:35 UTC

### Command to Reproduce

```bash
cd C:\Users\guilh\Desktop\proj
python -m pytest tests/test_contract_api_data.py -v
```

---

## Evidência Executável – RFC-001 Compliance

This evidence satisfies directive A1-6, section 1.7 requirements:

- ✅ **Test file exists in repository:** `tests/test_contract_api_data.py`
- ✅ **Validates contract (schema + status code + required fields):** 8 assertions cover response structure, field presence, types, and values
- ✅ **Execution log saved:** `pytest-contract-tests-20260621.log` with full output
- ✅ **Test runs and passes:** All 8 tests PASSED (100% success rate)

**Note:** Database is pre-populated with realistic sensor data from mock_main.py; contract tests verify that GET /data returns properly-formed JSON matching the schema defined in RFC-001 Section 5.2 (data flow scenario) and SRS FR-06 (functional requirement).

