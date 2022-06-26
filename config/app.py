import os

# Get API_TOKEN from environment variable
API_TOKEN = os.environ.get("API_TOKEN")

# Get CHANNEL_ID to forward messages to from environment variable
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# Get CHAT_ID to forward messages from, from environment variable
CHAT_ID = os.environ.get("CHAT_ID")

# Get DESCRIPTION from environment variable
DESCRIPTION = os.environ.get("DESCRIPTION")

# Either DEV or PROD environment
ENVIRONMENT = os.environ.get("ENVIRONMENT")

# Get DOMAIN from environment variable
DOMAIN = os.environ.get("DOMAIN")

# Get PORT from environment variable
PORT = os.environ.get("PORT")

# In seconds
SLEEPING_TIME = 30

# Total number of objects to be kept in database
MAX_OBJECTS = 1000

# Configure webhook
WEBHOOK_PATH = f"/webhook/{API_TOKEN}"
WEBHOOK_URL = f"https://{DOMAIN}{WEBHOOK_PATH}"
