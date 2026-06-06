DATABASE_PATH_STR:str = 'Database'
LOG_DATABASE_FILE_NAME:str = 'Logs.db'

# with open('src\\assets\\data_logs_db_wireframe.sql') as wireframe:
#   LOG_DATABASE_WIREFRAME:str = wireframe.read()

LOG_DATABASE_WIREFRAME:str = """
CREATE TABLE IF NOT EXISTS sensor_logs (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  recorded_at TEXT    NOT NULL DEFAULT (datetime('now')),
  temperature REAL,
  humidity REAL,
  ph REAL
);

CREATE INDEX IF NOT EXISTS idx_sensor_logs_recorded_at ON sensor_logs(recorded_at);
"""