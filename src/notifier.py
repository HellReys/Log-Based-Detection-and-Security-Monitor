import os
import requests


class TelegramNotifier():
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        if not self.token or not self.chat_id:
            print(f"❌ ERROR: Could not read information from .env file!")
        else:
            print(f"✅ Notifier Ready: Token and ChatID uploaded.")

    def send_alert(self, detection_result):
        if not self.token or not self.chat_id:
            return False

        message = (
            f"🚨 *SAFETY ALERT*\n\n"
            f"🔍 *Rule:* {detection_result['rule']}\n"
            f"🌐 *Source IP:* `{detection_result['ip']}`\n"
            f"📝 *Log:* `{detection_result['message']}`"
        )

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }

        try:
            response = requests.post(self.base_url, data=payload)

            if response.status_code != 200:
                print(f"❌ Telegram Error: {response.text}")

            return response.status_code == 200
        except Exception as e:
            print(f"❌ Notification could not be sent: {e}")
            return False