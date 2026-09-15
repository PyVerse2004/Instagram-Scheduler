from datetime import datetime
from pathlib import Path

from database import Base, SessionLocal, engine
from fake_publisher import FakePublisher
from media import Media, MediaType
from media_repository import MediaRepository
from scheduled_content import ContentType, ScheduledContent
from scheduled_content_repository import ScheduledContentRepository


def main():
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        media_repository = MediaRepository(session)
        repository = ScheduledContentRepository(session)

        media = Media(
            filename="scheduler-test.jpg",
            path=Path("media/scheduler-test.jpg"),
            media_type=MediaType.IMAGE,
        )

        media_model = media_repository.add(media)

        scheduled_content = ScheduledContent(
            media=media,
            content_type=ContentType.POST,
            publish_at=datetime(2026, 9, 15, 12, 0),
            caption="Scheduler test",
            hashtags=["python", "scheduler"],
        )

        content = repository.add(
            scheduled_content,
            media_id=media_model.id,
        )

        print("Created content:", content.id)
        print("Publish at:", content.publish_at)
        print("Status:", content.status)

        updated_content = repository.mark_publishing(content.id)

        print("After publishing:", updated_content.status)

        updated_content = repository.mark_published(content.id,datetime.utcnow(),)

        print("After published:", updated_content.status)
        print("Published at:", updated_content.published_at)

        try:
            repository.mark_publishing(content.id)
        except ValueError as exc:
            print("Invalid transition:", exc)


if __name__ == "__main__":
    main()