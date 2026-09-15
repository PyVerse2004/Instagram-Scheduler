from datetime import datetime
from pathlib import Path

from media import Media, MediaType
from scheduled_content import (
    ContentType,
    ScheduledContent,
)


def main():
    media = Media(
        filename="photo.jpg",
        path=Path("media/photo.jpg"),
        media_type=MediaType.IMAGE,
    )

    content = ScheduledContent(
        media=media,
        content_type=ContentType.POST,
        publish_at=datetime(2026, 9, 20, 18, 30),
        caption="My first scheduled post",
        hashtags=[
            "python",
            "instagram",
            "automation",
        ],
    )

    print("Caption:", content.caption)
    print("Hashtags:", content.hashtags)
    print("Retry count:", content.retry_count)
    print("Error:", content.error_message)
    print("Published at:", content.published_at)


if __name__ == "__main__":
    main()