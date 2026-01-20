import os
from dotenv import load_dotenv
from src.monitor import tail_file
from src.detector import DetectionEngine
from src.notifier import TelegramNotifier

load_dotenv()

def main():
    log_path = os.getenv("LOG_FILE_PATH")
    threshold = int(os.getenv("THRESHOLD"))

    print(f"--- Log Based Detection and Security Monitor started ---")
    print(f"--- File being monitored: {log_path} ---")

    engine = DetectionEngine()
    notifier = TelegramNotifier()

    try:
        for line in tail_file(log_path):
            result = engine.analyze(line)

            if result:
                # 1
                print(f"DETECTION: {result['rule']} | Source IP: {result['ip']}")
                # 2
                status = notifier.send_alert(result)

                if status:
                    print("📱 Notification sent successfully.")
                else:
                    print("⚠️ Notification failed (check logs).")

    except KeyboardInterrupt:
        print("\nThe system was shut down by the user. Stay safe!")



if __name__ == "__main__":
    main()