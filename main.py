import os
from dotenv import load_dotenv
from src.monitor import tail_file
from src.detector import DetectionEngine
from src.notifier import TelegramNotifier
from src.database import SecurityDB

load_dotenv()


def main():
    # Fetch configurations
    log_path = os.getenv("LOG_FILE_PATH")
    threshold = int(os.getenv("THRESHOLD"))

    print(f"--- 🛡️ Log-Based Detection & Security Monitor Started ---")
    print(f"--- 📂 Monitoring File: {log_path} ---")
    print(f"--- ⚙️ Security Threshold: {threshold} attempts ---")

    # Initialize professional modules
    db = SecurityDB()
    engine = DetectionEngine()
    notifier = TelegramNotifier()

    try:
        # Start continuous monitoring
        for line in tail_file(log_path):
            # Step 1: Analyze the log line for threats
            result = engine.analyze(line)

            if result:
                # Step 2: Save the event to the database (History/Logs)
                db.save_alert(result)

                # Step 3: Check how many times this IP has attacked in the last 5 minutes
                attack_count = db.get_ip_count(result['ip'], minutes=5)

                print(f"🔍 [LOG] IP: {result['ip']} | Attempt: {attack_count}/{threshold}")

                # Step 4: Decision Making (Logic)
                if attack_count >= threshold:
                    # Upgrade the alert level
                    result['rule'] = f"🚨 BRUTE FORCE DETECTED ({attack_count} attempts)"

                    # Step 5: Send Notification
                    status = notifier.send_alert(result)

                    if status:
                        print(f"📱 ALERT: Critical threat notification sent for IP: {result['ip']}")
                    else:
                        print(f"⚠️ ERROR: Failed to send Telegram notification.")

                # Optional: Even if it's below threshold, print a local warning
                elif attack_count == 1:
                    print(f"⚠️  WARNING: Initial threat detected from {result['ip']}")

    except KeyboardInterrupt:
        print("\n👋 System shut down by user. Security monitoring terminated.")
    except Exception as e:
        print(f"\n❌ CRITICAL SYSTEM ERROR: {e}")


if __name__ == "__main__":
    main()