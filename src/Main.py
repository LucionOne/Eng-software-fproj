from classes.DatabaseManager import DatabaseManager
from classes.dataPuller import DataPuller
import lib.logger as logger
from classes.APIService import app_builder
import uvicorn
import time
from typing import Generator


def main():
    # logger.setup_logging()
    # Puller = DataPuller()
    # Puller.Start()
    # cont:bool = True
    db = DatabaseManager()
    app = app_builder(db)
    uvicorn.run(app, host="0.0.0.0", port=3002)

    



if __name__ == '__main__':
    main()
