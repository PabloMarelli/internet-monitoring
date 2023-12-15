import os
import logging
import requests
import time
from telegram import Bot

# Initialize logging
log_directory = './log'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler(f'{log_directory}/internet_monitor.log', 'a', 'utf-8')])

# Replace with your own token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# Replace with your own chat ID
CHAT_ID = os.getenv('CHAT_ID')

# Initialize the bot
bot = Bot(TELEGRAM_BOT_TOKEN)

def check_internet():
    """Check internet connection by pinging google.com."""
    try:
        requests.get('https://www.google.com/', timeout=5)
        return True
    except requests.ConnectionError:
        return False
    except requests.ReadTimeout:
        logging.error("ReadTimeout error.")
        return False

# def send_telegram_message(message):
#     """Send a message to a specified Telegram chat."""
#     bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    logging.info("Internet monitoring started.")
    internet_status = True

    while True:
        current_status = check_internet()

        if current_status and not internet_status:
            # Internet just came back
            # send_telegram_message("Internet connection restored.")
            print("Internet connection restored.")
            logging.info("Internet connection restored.")
        elif not current_status and internet_status:
            # Internet just went down
            # send_telegram_message("Internet connection lost.")
            print("Internet connection lost.")
            logging.info("Internet connection lost.")

        internet_status = current_status
        time.sleep(1)  # Check every 60 seconds

if __name__ == '__main__':
    main()
