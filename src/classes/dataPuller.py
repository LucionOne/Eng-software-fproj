from classes.DatabaseManager import DatabaseManager
import logging
import queue
import requests
import threading
import time

log = logging.getLogger(__name__)

class DataPuller():
    """Pulls data from as API and writes it to the database"""
    def __init__(self) -> None:        
        self._fetcher_thread:threading.Thread = threading.Thread(target=self._fetcher, daemon= True)
        self._db_writer_thread:threading.Thread = threading.Thread(target=self._db_writer, daemon= True)
        self._queue:queue.Queue[dict] = queue.Queue()

        self.url:str = ""
        self.fetch_interval:int=300
        self.tries:int = 10

    def _fetcher(self) -> None:
        while True:
            for _try in range(self.tries):
                try:
                    resp = requests.get(self.url)
                    self._queue.put(resp.json())
                    break
                except Exception as e:
                    log.warning("Couldn't fetch data, try: %s details: %s", _try, e, exc_info=True)
            time.sleep(self.fetch_interval)

    def _db_writer(self) -> None:
        db_connection:DatabaseManager = DatabaseManager()
        while True:
            item = self._queue.get()
            try:
                self.save_to_db(item, db_connection)
            except Exception as e:
                    log.error("Write data to database, details: $s",e, exc_info=True)
            finally:
                self._queue.task_done()
                
    def Start(self) -> None:
        self._fetcher_thread.start()
        self._db_writer_thread.start()

    @staticmethod
    def save_to_db(item:dict, db:DatabaseManager) -> bool:
        query:str = """
        INSERT INTO sensor_logs(recorded_at, value, sensor_id)
        VALUES (?, ?, ?)
        """
        return False

