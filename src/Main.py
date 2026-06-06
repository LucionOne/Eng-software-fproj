from classes.DatabaseManager import DatabaseManager
from classes.dataPuller import DataPuller
import lib.logger as logger
import time


def main():
    logger.setup_logging()
    Puller = DataPuller()
    Puller.Start()
    time.sleep(60)




if __name__ == '__main__':
    main()
