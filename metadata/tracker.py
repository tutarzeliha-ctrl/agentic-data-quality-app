import sqlite3
from datetime import datetime
import pandas as pd

class MetadataTracker:
    def __init__(self, db_path="quality_metrics.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS execution_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                total_rows INTEGER,
                missing_values INTEGER,
                invalid_status INTEGER,
                quality_score REAL
            )
        """)
        conn.commit()
        conn.close()

    def log_run(self, total_rows, missing_values, invalid_status, quality_score):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO execution_logs (timestamp, total_rows, missing_values, invalid_status, quality_score)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, total_rows, missing_values, invalid_status, quality_score))
        conn.commit()
        conn.close()

    def get_history(self):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql("SELECT * FROM execution_logs ORDER BY timestamp DESC", conn)
        conn.close()
        return df