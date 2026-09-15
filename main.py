from database import Base, SessionLocal, engine
from fake_publisher import FakePublisher
from media_model import MediaModel
from scheduled_content_model import ScheduledContentModel
from scheduled_content_repository import ScheduledContentRepository
from scheduler_service import SchedulerService


def main():
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        repository = ScheduledContentRepository(session)
        publisher = FakePublisher()

        scheduler = SchedulerService(
            repository=repository,
            publisher=publisher,
        )

        content = repository.get_by_id(1)

        if content is None:
            print("Content not found.")
            return

        print("Before:", content.status)

        content = scheduler.retry(content.id)

        print("After retry:", content.status)

        content = scheduler.publish_content(content.id)

        print("After publish:", content.status)


if __name__ == "__main__":
    main()