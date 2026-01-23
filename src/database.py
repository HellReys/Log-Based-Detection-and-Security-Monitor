import sqlite3
from datetime import datetime

class SecurityDB:
    def __init__(self, db_name="security_events.db"):
        self.db_name = db_name
        self.setup_db()

    def setup_db(self):
        """Creates the tables."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                rule_name TEXT,
                ip_address TEXT,
                message TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_alert(self, detection_result):
        """It records the detected attack."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alerts (timestamp, rule_name, ip_address, message)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now(), detection_result['rule'], detection_result['ip'], detection_result['message']))
        conn.commit()
        conn.close()

    def get_ip_count(self, ip_address, minutes=5):
        """How many times has this IP address made an error in the last X minutes?"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM alerts 
            WHERE ip_address = ? AND timestamp > datetime('now', '-? minutes')
        ''', (ip_address, minutes))
        count = cursor.fetchone()[0]
        conn.close()
        return count