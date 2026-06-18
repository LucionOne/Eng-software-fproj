from classes.DatabaseManager import DatabaseManager
from enum import Enum
import logging
import queue
import requests
import threading
import time
from datetime import datetime

log = logging.getLogger(__name__)

class SensorType(Enum):
    Unknown = 0
    Temperature = 1
    Humidity = 2
    Ph = 3
    
    def __str__(self) -> str:
        match self.value:
            case SensorType.Temperature:
                return "Temperature"
            case SensorType.Humidity:
                return "Humidity"
            case SensorType.Ph:
                return "Ph"
            case _:
                return "Unknown"


    @staticmethod
    def from_string(value:str) -> SensorType:
        match value:
            case "Temperature":
                return SensorType.Temperature
            case "Humidity":
                return SensorType.Humidity
            case "Ph":
                return SensorType.Ph
            case _:
                return SensorType.Unknown
        


class DataPuller():
    """Pulls data from as API and writes it to the database"""
    def __init__(self) -> None:        
        self._fetcher_thread:threading.Thread = threading.Thread(target=self._fetcher, daemon= True)
        self._db_writer_thread:threading.Thread = threading.Thread(target=self._db_writer, daemon= True)
        self._queue:queue.Queue[dict] = queue.Queue()

        self.url:str = "http://localhost:3001/sensor_data"
        self.fetch_interval:int=5
        self.tries:int = 2

    def _fetcher(self) -> None:
        while True:
            try:
                resp = requests.get(self.url)
                self._queue.put(resp.json())
                print("fetched")
            except requests.exceptions.RequestException:
                print("no connection")
            except Exception as e:
                log.warning("Couldn't fetch data, url: %s\ntry: %s\nexception: %s", e, exc_info=True) # , self.url, _try
            time.sleep(self.fetch_interval)

    def _db_writer(self) -> None:
        db_connection:DatabaseManager = DatabaseManager()
        while True:
            item = self._queue.get()
            try:
                self.save_to_db(item, db_connection)
                print("wrote")
                # if not success: raise Exception
            except Exception as e:
                    log.error("Write data to database, details: $s",e, exc_info=True)
            finally:
                self._queue.task_done()
                
    def Start(self) -> None:
        self._fetcher_thread.start()
        self._db_writer_thread.start()

    @staticmethod
    def save_to_db(item:dict, db:DatabaseManager): # -> bool:
        query:str = """
        INSERT INTO sensor_logs(recorded_at, temperature, humidity, ph)
        VALUES (?, ?, ?, ?)
        """
        print(item)
        try:
            data = DataPuller._translate_from_api(item)
        except (KeyError, TypeError, ValueError) as e:
            log.error("invalid api payload; skipping db write: %s", e)
            return

        try:
            print(data)
            db.make_query(query, data)
        except Exception as e:
            log.critical('unable to make query %s', e)
        # return True
# -------
    @staticmethod
    def _translate_from_api(item: dict) -> tuple[str, float | None, float | None, float | None]:
        """Translate API item to (recorded_at, temperature, humidity, ph).
        API absolutely needs to give datetime in ISO 8601 format"""
        if not isinstance(item, dict):
            raise TypeError("api payload must be a dict")

        dt_str = item.get("datetime")
        if not isinstance(dt_str, str):
            raise TypeError("datetime must be a string")

        sensors = item.get("sensors")
        if not isinstance(sensors, list):
            raise ValueError("sensors must be a list")


        recorded_at = DataPuller._parse_datetime(dt_str)
        has_valid_sensor = False
        sensor_values: dict[SensorType, float | None] = {
            SensorType.Temperature: None,
            SensorType.Humidity: None,
            SensorType.Ph: None,
        }

        for sensor in sensors:
            try:
                sensor_type, value = DataPuller._validate_sensor_entry(sensor)
            except Exception as e:
                log.warning("Unable to extract data of sensor: %s %s", sensor, e)
                continue
            
            if not DataPuller._valid_values(sensor_type, value):
                log.warning("ignoring out-of-range value for sensor_type=%s: %s", sensor_type, value)
                continue
            
            if sensor_type not in sensor_values:
                log.warning("ignoring unknown sensor_type: %s", sensor.get("sensor_type"))
                continue
            
            current_value = sensor_values.get(sensor_type)
            if current_value is None:
                sensor_values[sensor_type] = value
                has_valid_sensor = True
            else:
                log.warning("multiple readings of %s; %s", sensor_type, value)

        if not has_valid_sensor:
            raise ValueError("no valid sensor measurements found in api payload")

        return (
            recorded_at,
            sensor_values[SensorType.Temperature],
            sensor_values[SensorType.Humidity],
            sensor_values[SensorType.Ph],
        )
    
    @staticmethod
    def _parse_datetime(value: str) -> str:
        """Validate that value is a valid ISO 8601 datetime string and return it."""
        if not isinstance(value, str):
            raise ValueError("datetime must be a string")

        try:
            normalized = value.replace("Z", "+00:00")
            datetime.fromisoformat(normalized)
        except Exception as e:
            raise ValueError(f"invalid ISO 8601 datetime: {value}") from e

        return normalized

    @staticmethod
    def _validate_sensor_entry(sensor: dict) -> tuple[SensorType, float | None]:
        """Validate sensor entry and return (SensorType, value)"""
        if not isinstance(sensor, dict):
            raise ValueError("each sensor entry must be a dict")

        sensor_type = sensor.get("sensor_type")
        if not isinstance(sensor_type, str):
            raise ValueError("sensor_type must be a string")

        value = sensor.get("value")
        if value is not None:
            try:
                parsed_value = float(value)
            except (TypeError, ValueError) as e:
                raise ValueError(f"sensor value must be numeric for sensor_type={sensor_type}") from e
        else:
            parsed_value = None

        sensor_enum = SensorType.from_string(sensor_type)
        return sensor_enum, parsed_value

    @staticmethod
    def _valid_values(measurement_type:SensorType, value:float|None) -> bool:
        """Verify that value is within expected range for given sensor type"""
        if value == None:
            return False
        if measurement_type == SensorType.Temperature:
            return -50 <= value <= 150
        elif measurement_type == SensorType.Humidity:
            return 0 <= value <= 100
        elif measurement_type == SensorType.Ph:
            return 0 <= value <= 14
        elif measurement_type == SensorType.Unknown:
            return False
# ------
