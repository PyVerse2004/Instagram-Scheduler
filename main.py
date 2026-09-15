from datetime import datetime
from pathlib import Path

from database import Base, SessionLocal, engine
from media import Media, MediaType
from media_model import MediaModel
from scheduled_content import ContentType, ScheduledContent
from scheduled_content_model import ScheduledContentModel
from scheduled_content_repository import ScheduledContentRepository


def main():
    Base.metadata.create_all(engine)

    with SessionLocal() as session:

        # Create a media record
        media_model = MediaModel(
            filename="photo.jpg",
            path="media/photo.jpg",
            media_type=MediaType.IMAGE.value,
            status="ready",
        )

        session.add(media_model)
        session.commit()
        session.refresh(media_model)

        # Create domain object
        media = Media(
            filename=media_model.filename,
            path=Path(media_model.path),
            media_type=MediaType(media_model.media_type),
        )

        scheduled_content = ScheduledContent(
            media=media,
            content_type=ContentType.POST,
            publish_at=datetime(2026, 9, 20, 18, 30),
            caption="My first scheduled post",
        )

        # Save scheduled content
        repository = ScheduledContentRepository(session)

        saved_content = repository.add(
            scheduled_content,
            media_id=media_model.id,
        )

        print(
            f"ID: {saved_content.id}"
        )

        print(
            f"Media ID: {saved_content.media_id}"
        )

        print(
            f"Type: {saved_content.content_type}"
        )

        print(
            f"Caption: {saved_content.caption}"
        )

        print(
            f"Publish at: {saved_content.publish_at}"
        )

        print(
            f"Status: {saved_content.status}"
        )


if __name__ == "__main__":
    main()