import threading
from fastapi import FastAPI, Depends
import uvicorn
from datetime import datetime, timedelta
from enum import Enum
import random as rand
from typing import Generator

# API instance creator
app = FastAPI(title="MockAPI", docs_url=None)

class SensorType(Enum):
    Unknown = 0
    Temperature = 1
    Humidity = 2
    Ph = 3
    
    def __str__(self) -> str:
        match self:
            case SensorType.Temperature:
                return "Temperature"
            case SensorType.Humidity:
                return "Humidity"
            case SensorType.Ph:
                return "Ph"
            case _:
                return "Unknown"

class Sensor():
    def __init__(self, id:int, type:SensorType) -> None:
        self.value:float = 0
        self.id:int = id
        self.type:SensorType = type
        

    def serialize(self) -> dict:
        base_dict:dict = {"sensor_id":None, "sensor_type":None, "value": None}
        base_dict["sensor_id"] = self.id
        base_dict["sensor_type"] = str(self.type)
        base_dict["value"] = round(self.value,2)
        return base_dict

class Simulation():
    def __init__(self) -> None:
        self._thread = threading.Thread(target=self.simulation, daemon = True)

        self.datetime:datetime = self.get_time()
        self.clock:timedelta = timedelta(minutes=5)

        self.recorded:bool = False
        self.create_sensors()


    def create_sensors(self) -> None:
        sensorH:Sensor = Sensor(1, SensorType.Temperature)
        sensorT:Sensor = Sensor(2, SensorType.Humidity)
        sensorP:Sensor = Sensor(3, SensorType.Ph)
        self.sensors:list[Sensor] = [sensorH, sensorT, sensorP]
        

    def get_time(self) -> datetime:
        try:
            with open("C:\\Users\\guilh\\Desktop\\proj\\mock\\memory.txt", "r") as file:
                return datetime.fromisoformat(file.read())
        except:
            return datetime.now()


    def write_time(self) -> None:
        with open("C:\\Users\\guilh\\Desktop\\proj\\mock\\memory.txt", "w") as file:
            file.write(self.datetime.isoformat())

    
    def run_sim(self) -> None:
        self._thread.start()

            
    def simulation(self) -> None:
        ranges = {
            SensorType.Temperature: (-50.0, 150.0),
            SensorType.Humidity: (0.0, 100.0),
            SensorType.Ph: (0.0, 14.0),
        }

        while True:
            if self.recorded:
                self.datetime += self.clock
                self.write_time() # yeah... whatever i'm tired now ;-;
                for sensor in self.sensors:
                    min_val, max_val = ranges.get(sensor.type, (-9999.0, 9999.0))
                    sensor.value += rand.uniform(-5.0, 5.0)
                    sensor.value = max(min_val, min(sensor.value, max_val))
                print("simulated")
                self.recorded = False


# Start of script
if __name__ == "__main__":
    main_instance = Simulation()
    main_instance.run_sim()

# API get
def get_db() -> Generator[Simulation]:
    yield main_instance
    
@app.get("/sensor_data")
def get_data(instance:Simulation = Depends(get_db)) -> dict:
    sensor_dict = {}
    sensor_dict["sensors"] = [sensor.serialize() for sensor in instance.sensors]
    sensor_dict["datetime"] = instance.datetime.isoformat()
    instance.recorded = True
    print (sensor_dict)
    return sensor_dict

# Runs the API 
uvicorn.run(app, host="0.0.0.0", port=3001)
