import sqlite3
import os
from datetime import datetime, timezone

class SecurityDB:
    def __init__(self, db_folder="db", db_name="security_events.db"):
        self.db_folder = db_folder
        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)
            print(f"📁 Created directory: {self.db_folder}")

        self.db_path = os.path.join(self.db_folder, db_name)
        self.setup_db()

    def setup_db(self):
        """Creates the table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
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
        """Saves the event to the database in the db/ folder."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alerts (timestamp, rule_name, ip_address, message)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now(timezone.utc), detection_result['rule'], detection_result['ip'], detection_result['message']))
        conn.commit()
        conn.close()

    def get_ip_count(self, ip_address, minutes=5):
        """Counts alerts within the last X minutes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM alerts WHERE ip_address = ? AND timestamp > datetime('now', '-{minutes} minutes')"

        try:
            cursor.execute(query, (ip_address,))
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            print(f"❌ Database Query Error: {e}")
            return 0
        finally:
            conn.close()
            return count