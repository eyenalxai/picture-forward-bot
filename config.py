import os

# Get API_TOKEN from environment variable
API_TOKEN = os.environ.get("API_TOKEN")

# Get CHANNEL_ID to forward messages to from environment variable
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# Get CHAT_ID to forward messages from, from environment variable
CHAT_ID = os.environ.get("CHAT_ID")

# Get SOURCE_URL to forward messages to from environment variable
SOURCE_URL = os.environ.get("SOURCE_URL")
