import pytest
import sys
from pathlib import Path

# Add src directory to path so imports work correctly
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from classes.dataPuller import DataPuller, SensorType


class TestTranslateFromApiValidInputs:
    """Tests for valid JSON inputs"""

    def test_valid_single_sensor_temperature(self):
        """Test valid payload with only temperature sensor"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": 25.5}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[0] == "2024-01-15T10:30:00+00:00"
        assert result[1] == 25.5
        assert result[2] is None
        assert result[3] is None

    def test_valid_single_sensor_humidity(self):
        """Test valid payload with only humidity sensor"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Humidity", "value": 65.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[0] == "2024-01-15T10:30:00+00:00"
        assert result[1] is None
        assert result[2] == 65.0
        assert result[3] is None

    def test_valid_single_sensor_ph(self):
        """Test valid payload with only pH sensor"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Ph", "value": 7.2}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[0] == "2024-01-15T10:30:00+00:00"
        assert result[1] is None
        assert result[2] is None
        assert result[3] == 7.2

    def test_valid_all_sensors(self):
        """Test valid payload with all three sensors"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": 22.5},
                {"sensor_type": "Humidity", "value": 55.0},
                {"sensor_type": "Ph", "value": 6.8}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[0] == "2024-01-15T10:30:00+00:00"
        assert result[1] == 22.5
        assert result[2] == 55.0
        assert result[3] == 6.8

    def test_valid_iso8601_with_z_timezone(self):
        """Test valid ISO 8601 datetime with Z timezone"""
        payload = {
            "datetime": "2024-01-15T10:30:00Z",
            "sensors": [
                {"sensor_type": "Temperature", "value": 20.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[0] == "2024-01-15T10:30:00+00:00"
        assert result[1] == 20.0

    def test_valid_string_numeric_values(self):
        """Test that string numeric values are converted to float"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": "23.7"},
                {"sensor_type": "Humidity", "value": "45"},
                {"sensor_type": "Ph", "value": "7"}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == 23.7
        assert result[2] == 45.0
        assert result[3] == 7.0

    def test_valid_integer_values(self):
        """Test that integer values are converted to float"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": 25},
                {"sensor_type": "Humidity", "value": 60}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == 25.0
        assert result[2] == 60.0

    def test_valid_null_sensor_value(self):
        """Test sensor with null value is treated as None"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": None},
                {"sensor_type": "Humidity", "value": 50.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] is None
        assert result[2] == 50.0

    def test_valid_edge_case_temperature_min(self):
        """Test temperature at minimum valid value"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": -50.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == -50.0

    def test_valid_edge_case_temperature_max(self):
        """Test temperature at maximum valid value"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": 150.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == 150.0

    def test_valid_edge_case_humidity_min(self):
        """Test humidity at minimum valid value"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Humidity", "value": 0.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[2] == 0.0

    def test_valid_edge_case_humidity_max(self):
        """Test humidity at maximum valid value"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Humidity", "value": 100.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[2] == 100.0

    def test_valid_edge_case_ph_min(self):
        """Test pH at minimum valid value"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Ph", "value": 0.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[3] == 0.0

    def test_valid_edge_case_ph_max(self):
        """Test pH at maximum valid value"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Ph", "value": 14.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[3] == 14.0

    def test_valid_with_extra_fields_in_payload(self):
        """Test that extra fields in payload are ignored"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": 25.0}
            ],
            "extra_field": "ignored",
            "another_field": 12345
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == 25.0

    def test_valid_with_extra_fields_in_sensor(self):
        """Test that extra fields in sensor are ignored"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": 25.0, "extra": "data", "unit": "C"}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == 25.0


class TestTranslateFromApiInvalidInputs:
    """Tests for invalid JSON inputs - expecting exceptions"""

    def test_invalid_not_a_dict(self):
        """Test that non-dict input raises TypeError"""
        with pytest.raises(TypeError, match="api payload must be a dict"):
            DataPuller._translate_from_api("not a dict")

    def test_invalid_list_input(self):
        """Test that list input raises TypeError"""
        with pytest.raises(TypeError, match="api payload must be a dict"):
            DataPuller._translate_from_api([])

    def test_invalid_none_input(self):
        """Test that None input raises TypeError"""
        with pytest.raises(TypeError, match="api payload must be a dict"):
            DataPuller._translate_from_api(None)

    def test_invalid_integer_input(self):
        """Test that integer input raises TypeError"""
        with pytest.raises(TypeError, match="api payload must be a dict"):
            DataPuller._translate_from_api(42)

    def test_invalid_missing_datetime(self):
        """Test that missing datetime raises TypeError"""
        payload = {
            "sensors": [
                {"sensor_type": "Temperature", "value": 25.0}
            ]
        }
        with pytest.raises(TypeError, match="datetime must be a string"):
            DataPuller._translate_from_api(payload)

    def test_invalid_datetime_not_string(self):
        """Test that non-string datetime raises TypeError"""
        payload = {
            "datetime": 12345,
            "sensors": [
                {"sensor_type": "Temperature", "value": 25.0}
            ]
        }
        with pytest.raises(TypeError, match="datetime must be a string"):
            DataPuller._translate_from_api(payload)

    def test_invalid_datetime_none(self):
        """Test that None datetime raises TypeError"""
        payload = {
            "datetime": None,
            "sensors": [
                {"sensor_type": "Temperature", "value": 25.0}
            ]
        }
        with pytest.raises(TypeError, match="datetime must be a string"):
            DataPuller._translate_from_api(payload)

    def test_invalid_datetime_format(self):
        """Test that invalid ISO 8601 datetime raises ValueError"""
        payload = {
            "datetime": "2024-13-45T99:99:99",
            "sensors": [
                {"sensor_type": "Temperature", "value": 25.0}
            ]
        }
        with pytest.raises(ValueError, match="invalid ISO 8601 datetime"):
            DataPuller._translate_from_api(payload)

    def test_invalid_datetime_random_string(self):
        """Test that random string datetime raises ValueError"""
        payload = {
            "datetime": "not a datetime",
            "sensors": [
                {"sensor_type": "Temperature", "value": 25.0}
            ]
        }
        with pytest.raises(ValueError, match="invalid ISO 8601 datetime"):
            DataPuller._translate_from_api(payload)

    def test_invalid_missing_sensors(self):
        """Test that missing sensors raises ValueError"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00"
        }
        with pytest.raises(ValueError, match="sensors must be a list"):
            DataPuller._translate_from_api(payload)

    def test_invalid_sensors_not_list(self):
        """Test that non-list sensors raises ValueError"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": {"sensor_type": "Temperature", "value": 25.0}
        }
        with pytest.raises(ValueError, match="sensors must be a list"):
            DataPuller._translate_from_api(payload)

    def test_invalid_sensors_string(self):
        """Test that string sensors raises ValueError"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": "not a list"
        }
        with pytest.raises(ValueError, match="sensors must be a list"):
            DataPuller._translate_from_api(payload)

    def test_invalid_sensors_none(self):
        """Test that None sensors raises ValueError"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": None
        }
        with pytest.raises(ValueError, match="sensors must be a list"):
            DataPuller._translate_from_api(payload)

    def test_invalid_empty_sensors_list(self):
        """Test that empty sensors list raises ValueError"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": []
        }
        with pytest.raises(ValueError, match="no valid sensor measurements found"):
            DataPuller._translate_from_api(payload)

    def test_invalid_sensor_not_dict(self):
        """Test that non-dict sensor entry is skipped, but valid sensors pass"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                "not a dict",
                {"sensor_type": "Temperature", "value": 25.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == 25.0

    def test_invalid_sensor_missing_sensor_type(self):
        """Test that sensor without sensor_type is skipped"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"value": 25.0},
                {"sensor_type": "Humidity", "value": 50.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[2] == 50.0

    def test_invalid_sensor_type_not_string(self):
        """Test that non-string sensor_type is skipped"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": 123, "value": 25.0},
                {"sensor_type": "Humidity", "value": 50.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[2] == 50.0

    def test_invalid_sensor_value_not_numeric(self):
        """Test that non-numeric sensor value is skipped"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": "not a number"},
                {"sensor_type": "Humidity", "value": 50.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] is None
        assert result[2] == 50.0

    def test_invalid_temperature_below_range(self):
        """Test that temperature below -50 is skipped"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": -51.0},
                {"sensor_type": "Humidity", "value": 50.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] is None
        assert result[2] == 50.0

    def test_invalid_temperature_above_range(self):
        """Test that temperature above 150 is skipped"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": 151.0},
                {"sensor_type": "Humidity", "value": 50.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] is None
        assert result[2] == 50.0

    def test_invalid_humidity_below_range(self):
        """Test that humidity below 0 is skipped"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Humidity", "value": -1.0},
                {"sensor_type": "Temperature", "value": 25.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == 25.0
        assert result[2] is None

    def test_invalid_humidity_above_range(self):
        """Test that humidity above 100 is skipped"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Humidity", "value": 101.0},
                {"sensor_type": "Temperature", "value": 25.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == 25.0
        assert result[2] is None

    def test_invalid_ph_below_range(self):
        """Test that pH below 0 is skipped"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Ph", "value": -0.1},
                {"sensor_type": "Temperature", "value": 25.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == 25.0
        assert result[3] is None

    def test_invalid_ph_above_range(self):
        """Test that pH above 14 is skipped"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Ph", "value": 14.1},
                {"sensor_type": "Temperature", "value": 25.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == 25.0
        assert result[3] is None

    def test_invalid_unknown_sensor_type(self):
        """Test that unknown sensor type is skipped"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "UnknownType", "value": 25.0},
                {"sensor_type": "Temperature", "value": 20.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == 20.0

    def test_invalid_all_sensors_skipped(self):
        """Test that error is raised when all sensors are invalid"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": -100.0},
                {"sensor_type": "Humidity", "value": "not a number"},
                {"sensor_type": "Ph", "value": 20.0}
            ]
        }
        with pytest.raises(ValueError, match="no valid sensor measurements found"):
            DataPuller._translate_from_api(payload)

    def test_invalid_duplicate_sensor_type_first_wins(self):
        """Test that first reading of duplicate sensor type is kept"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                {"sensor_type": "Temperature", "value": 25.0},
                {"sensor_type": "Temperature", "value": 30.0}
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == 25.0

    def test_invalid_mixed_valid_and_invalid_sensors(self):
        """Test that invalid sensors are logged and skipped, valid ones processed"""
        payload = {
            "datetime": "2024-01-15T10:30:00+00:00",
            "sensors": [
                "invalid",
                {"sensor_type": "Temperature", "value": 25.0},
                {"sensor_type": 123},
                {"sensor_type": "Humidity", "value": 55.0},
                None
            ]
        }
        result = DataPuller._translate_from_api(payload)
        assert result[1] == 25.0
        assert result[2] == 55.0
