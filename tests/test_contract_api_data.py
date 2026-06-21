import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from classes.APIService import app_builder

@pytest.fixture
def client():
    """Create FastAPI test client with app"""
    app = app_builder()
    return TestClient(app)

class TestContractGetDataEndpoint:
    """Provider-side contract tests for GET /data endpoint (RFC-001 ADR-001 boundary contract)"""

    def test_get_data_returns_200_status(self, client):
        """Verify GET /data returns HTTP 200 OK"""
        response = client.get("/data")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    def test_get_data_response_is_json(self, client):
        """Verify GET /data response is valid JSON with correct content-type"""
        response = client.get("/data")
        assert response.headers.get("content-type") == "application/json"
        # Verify it can be deserialized
        data = response.json()
        assert isinstance(data, dict), "Response body must be JSON dict"

    def test_get_data_has_required_top_level_schema(self, client):
        """Verify GET /data response contains required top-level fields"""
        response = client.get("/data")
        data = response.json()
        
        # Per RFC-001 FR-06 and SRS UC-01: response must have status, data
        assert "status" in data, "Response must include 'status' field"
        assert data["status"] == "ok", f"Status must be 'ok', got '{data['status']}'"
        assert "data" in data, "Response must include 'data' field"

    def test_get_data_response_structure(self, client):
        """Verify GET /data response structure matches contract (RFC-001 wireframe 1)"""
        response = client.get("/data")
        data = response.json()
        
        # Validate nested data object
        assert isinstance(data["data"], dict), "'data' field must be a dict"
        assert "readings" in data["data"], "data.readings required"
        assert "latest_id" in data["data"], "data.latest_id required"
        assert "count" in data["data"], "data.count required"
        
        assert isinstance(data["data"]["readings"], list), "readings must be list"
        assert isinstance(data["data"]["count"], int), "count must be int"
        # latest_id can be int or null (per UC-01 alternative 1a: empty database)
        assert data["data"]["latest_id"] is None or isinstance(data["data"]["latest_id"], int), \
            "latest_id must be int or null"

    def test_get_data_reading_schema_has_required_fields(self, client):
        """Verify each reading in response has required fields (recorded_at, temperature, humidity, ph)"""
        response = client.get("/data")
        data = response.json()
        readings = data["data"]["readings"]
        
        # If database is empty, readings may be empty list — that's OK (UC-01 alternative 1a)
        if len(readings) > 0:
            reading = readings[0]
            # Per RFC-001 Section 5.2 data flow and SRS UC-01 wireframe
            # Actual schema uses recorded_at (not timestamp) as defined in SQL_config.py
            required_fields = ["id", "recorded_at", "temperature", "humidity", "ph"]
            for field in required_fields:
                assert field in reading, f"Reading must include '{field}' field"
            
            # Type validation
            assert isinstance(reading["id"], int), "id must be int"
            assert isinstance(reading["recorded_at"], str), "recorded_at must be string (ISO 8601)"
            # Sensor values can be float, int, or None (if not present or invalid)
            assert reading["temperature"] is None or isinstance(reading["temperature"], (int, float))
            assert reading["humidity"] is None or isinstance(reading["humidity"], (int, float))
            assert reading["ph"] is None or isinstance(reading["ph"], (int, float))

    def test_get_data_with_after_id_parameter(self, client):
        """Verify GET /data?after_id=N returns proper subset (RFC-001 UC-02 contract)"""
        response = client.get("/data?after_id=999")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "readings" in data["data"]
        # If database has <999 records, readings should be empty
        # (we don't know actual db state, so just verify structure is valid)
        assert isinstance(data["data"]["readings"], list)

    def test_get_data_count_matches_readings_length(self, client):
        """Verify count field matches actual length of readings array"""
        response = client.get("/data")
        data = response.json()
        readings = data["data"]["readings"]
        count = data["data"]["count"]
        
        assert count == len(readings), \
            f"count={count} does not match readings length={len(readings)}"

    def test_get_data_latest_id_reflects_last_reading(self, client):
        """Verify latest_id is max of all reading ids, or null if empty"""
        response = client.get("/data")
        data = response.json()
        readings = data["data"]["readings"]
        latest_id = data["data"]["latest_id"]
        
        if len(readings) == 0:
            assert latest_id is None, "latest_id should be null when readings is empty"
        else:
            max_id = max(r["id"] for r in readings)
            assert latest_id == max_id, f"latest_id={latest_id} should equal max reading id={max_id}"
