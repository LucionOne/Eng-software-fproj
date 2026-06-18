from classes.DatabaseManager import DatabaseManager
from classes.dataPuller import DataPuller
import lib.logger as logger
from classes.APIService import app_builder
import uvicorn



def main():
    logger.setup_logging()

    Puller = DataPuller()
    Puller.Start()

    # db = DatabaseManager()
    app = app_builder()

    uvicorn.run(app, host="0.0.0.0", port=3002)

    # db.close_connection()


if __name__ == '__main__':
    main()
