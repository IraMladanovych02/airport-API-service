import os
import logging
import requests
from typing import NoReturn
logger = logging.getLogger(__name__)


TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message: str) -> NoReturn:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram token or chat_id not configured.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(url, data=payload, timeout=5)
        response.raise_for_status()
        logger.info("Telegram message sent successfully.")
    except requests.RequestException as e:
        logger.error(f"Failed to send Telegram message: {e}")
