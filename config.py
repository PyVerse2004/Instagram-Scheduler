from dotenv import load_dotenv
import os

load_dotenv()

SCHEDULER_INTERVAL_SECONDS = int(
    os.getenv("SCHEDULER_INTERVAL_SECONDS", "10")
)

MAX_RETRIES = int(
    os.getenv("MAX_RETRIES", "3")
)

PUBLISHING_TIMEOUT_SECONDS = int(
    os.getenv("PUBLISHING_TIMEOUT_SECONDS", "300")
)

MEDIA_FOLDER = os.getenv(
    "MEDIA_FOLDER",
    "media",
)

# Instagram
INSTAGRAM_ACCESS_TOKEN = os.getenv(
    "INSTAGRAM_ACCESS_TOKEN",
    "",
)

INSTAGRAM_ACCOUNT_ID = os.getenv(
    "INSTAGRAM_ACCOUNT_ID",
    "",
)