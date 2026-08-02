import requests
from src.config import Config

def send_webhook_notification(content: str) -> bool:
    webhook_url = Config.WEBHOOK_URL
    if not webhook_url:
        return False
        
    print("🔔 Sending notification via Webhook...")
    try:
        # Generic Markdown/Text payload
        payload = {"text": content[:2000], "content": content[:2000]}
        res = requests.post(webhook_url, json=payload, timeout=10)
        if res.status_code in [200, 204]:
            print("✅ Webhook notification sent successfully!")
            return True
        else:
            print(f"⚠️ Webhook response error: {res.status_code} - {res.text}")
            return False
    except Exception as e:
        print(f"⚠️ Failed to send webhook: {e}")
        return False
