import os

# Get API_TOKEN from environment variable
from urllib.parse import urljoin

API_TOKEN = os.environ.get("API_TOKEN")

# Get CHANNEL_ID to forward messages to from environment variable
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# Get PROJECT_NAME from environment variable
PROJECT_NAME = os.environ.get("PROJECT_NAME")

# Get PORT from environment variable
PORT = os.environ.get("PORT")

HOST = "0.0.0.0"
WEBHOOK_HOST = f'https://{PROJECT_NAME}.up.railway.app/'  # Enter here your link from Heroku project settings

WEBHOOK_URL_PATH = '/webhook/' + API_TOKEN
WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_URL_PATH)
