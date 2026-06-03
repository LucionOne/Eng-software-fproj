DATABASE_PATH_STR:str = 'Database'
LOG_DATABASE_FILE_NAME:str = 'Logs.db'

# with open('src\\assets\\data_logs_db_wireframe.sql') as wireframe:
#   LOG_DATABASE_WIREFRAME:str = wireframe.read()

LOG_DATABASE_WIREFRAME:str = """
CREATE TABLE IF NOT EXISTS measurement_types (
  id    INTEGER PRIMARY KEY AUTOINCREMENT,
  name  TEXT    NOT NULL UNIQUE
);

INSERT OR IGNORE INTO measurement_types (name) VALUES
('Unknown'),
('Temperature'),
('Humidity'),
('Ph');


CREATE TABLE IF NOT EXISTS sensors (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  model   TEXT    NOT NULL,
  type_id INTEGER NOT NULL REFERENCES measurement_types(id) ON DELETE RESTRICT
);


CREATE TABLE IF NOT EXISTS sensor_logs (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  recorded_at TEXT    NOT NULL DEFAULT (datetime('now')),
  value       REAL,
  sensor_id   INTEGER NOT NULL REFERENCES sensors(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS maintenance_logs (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  maintenance_at  TEXT    NOT NULL,
  description     TEXT    NOT NULL,
  sensor_id       INTEGER REFERENCES sensors(id) ON DELETE SET NULL
);


CREATE INDEX IF NOT EXISTS idx_sensors_type_id ON sensors(type_id);
CREATE INDEX IF NOT EXISTS idx_sensor_logs_sensor_id ON sensor_logs(sensor_id);
CREATE INDEX IF NOT EXISTS idx_sensor_logs_recorded_at ON sensor_logs(recorded_at);
CREATE INDEX IF NOT EXISTS idx_maintenance_logs_sensor_id ON maintenance_logs(sensor_id);
"""