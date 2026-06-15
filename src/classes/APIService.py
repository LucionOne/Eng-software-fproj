from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from classes.DatabaseManager import DatabaseManager
from typing import Generator

# uvicorn.run(app, host="0.0.0.0", port=3001)
def app_builder(db:DatabaseManager) -> FastAPI:
    app = FastAPI(title= "TBD")
    def get_db() -> Generator[DatabaseManager]:
        yield db
    
    @app.get("/", response_class=HTMLResponse)
    def get_html() -> HTMLResponse:
        with open("src\\assets\\dashboard.html", encoding='utf-8') as page:
            html = page.read()
        return HTMLResponse(html, status_code= 200)
    
    @app.get("/data")
    def get_data(db:DatabaseManager = Depends(get_db)) -> list[dict]:
        readings = db.fetch_data("SELECT * FROM sensor_logs")
        return readings
    
    @app.get("/data/{date}")
    def get_data_since(date:str, db:DatabaseManager = Depends(get_db)) -> list[dict]:
        readings = db.fetch_data("SELECT * FROM sensor_logs WHERE recorded_at > ?",(date))
        return readings
    
    return app