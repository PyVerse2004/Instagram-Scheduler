import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from config import SCHEDULER_INTERVAL_SECONDS
from database import Base, SessionLocal, engine
from fake_publisher import FakePublisher
from media_model import MediaModel
from scheduled_content_repository import ScheduledContentRepository
from scheduler_service import SchedulerService
from time_utils import utc_now


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def check_and_publish():
    logger.info("Checking for due content.")

    with SessionLocal() as session:
        repository = ScheduledContentRepository(session)
        publisher = FakePublisher()

        scheduler_service = SchedulerService(
            repository=repository,
            publisher=publisher,
        )

        now = utc_now()

        recovered = scheduler_service.recover_stale_publishing(
            now
        )

        logger.info(
            "Recovered %s stale publishing item(s).",
            len(recovered),
        )

        due_content = scheduler_service.get_due_content(
            now
        )

        logger.info(
            "Found %s due content item(s).",
            len(due_content),
        )

        for content in due_content:
            scheduler_service.publish_content(
                content.id
            )


def start_scheduler():
    Base.metadata.create_all(engine)

    scheduler = BlockingScheduler()

    scheduler.add_job(
        check_and_publish,
        "interval",
        seconds=SCHEDULER_INTERVAL_SECONDS,
        id="publish_due_content",
        max_instances=1,
        coalesce=True,
    )

    logger.info(
        "Scheduler started. Interval: %s seconds.",
        SCHEDULER_INTERVAL_SECONDS,
    )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    start_scheduler()