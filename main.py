from datetime import datetime

from database import Base, SessionLocal, engine
from scheduled_content_repository import ScheduledContentRepository
from scheduler_service import SchedulerService


def main():
    Base.metadata.create_all(engine)

    now = datetime(2026, 9, 20, 19, 00)

    with SessionLocal() as session:
        repository = ScheduledContentRepository(session)
        scheduler = SchedulerService(repository)

        due_content = scheduler.get_due_content(now)

        print(f"Current time: {now}")
        print(f"Due content count: {len(due_content)}")

        for content in due_content:
            print(
                f"{content.id} | "
                f"{content.content_type} | "
                f"{content.publish_at} | "
                f"{content.status}"
            )


if __name__ == "__main__":
    main()