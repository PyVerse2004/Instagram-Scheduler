from datetime import datetime
from pathlib import Path

from database import Base, SessionLocal, engine
from fake_publisher import FakePublisher
from media import Media, MediaType
from media_model import MediaModel
from scheduled_content import ContentType, ScheduledContent
from scheduled_content_model import ScheduledContentModel
from scheduled_content_repository import ScheduledContentRepository
from scheduler_service import SchedulerService
from media_repository import MediaRepository


def main():
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        repository = ScheduledContentRepository(session)
        media_repository = MediaRepository(session)

        # Create media
        media = Media(
            filename="photo.jpg",
            path=Path("media/photo.jpg"),
            media_type=MediaType.IMAGE,
        )

        media_model = media_repository.add(media)

        # Create scheduled content
        scheduled_content = ScheduledContent(
            media=media,
            content_type=ContentType.POST,
            publish_at=datetime(2026, 9, 20, 18, 30),
            caption="Test publishing",
            hashtags=[
                "python",
                "instagram",
                "automation",
            ],
        )

        content = repository.add(
            scheduled_content,
            media_id=media_model.id,
        )

        print("Initial status:", content.status)

        # Publisher
        publisher = FakePublisher(should_fail=True)

        scheduler = SchedulerService(
            repository=repository,
            publisher=publisher,
        )

        # Publish
        content = scheduler.publish_content(content.id)

        print("Status:", content.status)
        print("Published at:", content.published_at)
        print("Retry count:", content.retry_count)
        print("Error:", content.error_message)

        # Retry
        content = scheduler.retry(content.id)

        print("After retry:", content.status)


if __name__ == "__main__":
    main()