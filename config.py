import os

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
    "media"
)

SUPPORTED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

SUPPORTED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
}

INSTAGRAM_ACCESS_TOKEN = os.getenv(
    "INSTAGRAM_ACCESS_TOKEN",
    "",
)

INSTAGRAM_ACCOUNT_ID = os.getenv(
    "INSTAGRAM_ACCOUNT_ID",
    "",
)