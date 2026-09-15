from time_utils import utc_now
from media_model import MediaModel
from apscheduler.schedulers.blocking import BlockingScheduler

from database import SessionLocal
from fake_publisher import FakePublisher
from scheduled_content_repository import ScheduledContentRepository
from scheduler_service import SchedulerService


def check_and_publish():
    with SessionLocal() as session:
        repository = ScheduledContentRepository(session)
        publisher = FakePublisher()

        scheduler_service = SchedulerService(
            repository=repository,
            publisher=publisher,
        )

        now = utc_now()

        due_content = scheduler_service.get_due_content(now)

        for content in due_content:
            scheduler_service.publish_content(content.id)


def start_scheduler():
    scheduler = BlockingScheduler()

    scheduler.add_job(
        check_and_publish,
        "interval",
        seconds=10,
    )

    print("Scheduler started.")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")

if __name__ == "__main__":
    start_scheduler()