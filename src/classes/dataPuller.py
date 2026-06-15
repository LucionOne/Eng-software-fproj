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
                success = self.save_to_db(item, db_connection)
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
        data = DataPuller.translate_from_api(item)
        try:
            print(data)
            db.make_query(query, data)
        except Exception as e:
            log.critical('unable to make query %s', e)
        # return True


    @staticmethod
    def translate_from_api(item: dict) -> tuple[str, float, float, float]:
        """Translate API item to (recorded_at, temperature, humidity, ph).
        API absolutely needs to give datetime in ISO 8601 format"""
        try:
            sensors: list[dict] = item["sensors"]
            recorded_at: str = item["datetime"]
            temperature: float = 0.0
            humidity: float = 0.0
            ph: float = 0.0
            for sensor in sensors:
                st = SensorType.from_string(sensor["sensor_type"])  # st = SensorType.from_string(sensor.get("sensor_type", ""))
                if st == SensorType.Temperature:
                    temperature = float(sensor["value"])
                elif st == SensorType.Humidity:
                    humidity = float(sensor["value"])
                elif st == SensorType.Ph:
                    ph = float(sensor["value"])

            return (recorded_at, temperature, humidity, ph)
        except Exception as e:
            log.critical("couldn't translate data from api %s", e, exc_info=True)
            raise
