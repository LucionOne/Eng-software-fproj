from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from classes.DatabaseManager import DatabaseManager
from typing import Generator

# uvicorn.run(app, host="0.0.0.0", port=3001)
def app_builder() -> FastAPI:
    # db = DatabaseManager()
    app = FastAPI(title= "TBD")

    # def get_db() -> Generator[DatabaseManager]:
    #     yield db
    
    @app.get("/", response_class=HTMLResponse)
    def get_html() -> HTMLResponse:
        with open("src\\assets\\dashboard.html", encoding='utf-8') as page:
            html = page.read()
        return HTMLResponse(html, status_code= 200)
# json format
# {
#   "status": "ok",
#   "data": {
#     "readings": [
#       {
#         "id": 1,
#         "timestamp": "2024-06-14T10:00:00.000Z",
#         "temperature": 23.5,
#         "humidity": 65.2,
#         "ph": 7.1
#       }
#     ],
#     "latest_id": 100,
#     "count": 100
#   }
# }

    @app.get("/data")
    def get_data(): #db:DatabaseManager = Depends(get_db)) -> dict:
        db = DatabaseManager()
        readings = db.fetch_data("SELECT * FROM sensor_logs")
        count = db.fetch_data("SELECT COUNT(*) as count FROM sensor_logs")[0]["count"] if readings else 0
        latest_id = db.fetch_data("SELECT MAX(id) as latest_id FROM sensor_logs")[0]["latest_id"] if readings else None
        db.close_connection()

        return {
            "status": "ok",
            "data": {
                "readings": [dict(row) for row in readings],
                "latest_id": latest_id,
                "count": count
            }
        }
    
    @app.get("/data/{date}")
    def get_data_since(date:str):#, db:DatabaseManager = Depends(get_db)) -> dict:
        db = DatabaseManager()
        readings = db.fetch_data("SELECT * FROM sensor_logs WHERE recorded_at > ?", (date,))
        count = len(readings)
        latest_id = db.fetch_data("SELECT MAX(id) as latest_id FROM sensor_logs WHERE recorded_at > ?", (date,))[0]["latest_id"] if readings else None
        db.close_connection()
        
        return {
            "status": "ok",
            "data": {
                "readings": [dict(row) for row in readings],
                "latest_id": latest_id,
                "count": count
            }
        }
    
    return app