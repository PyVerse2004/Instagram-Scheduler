from datetime import datetime
import logging

from config import MAX_RETRIES
from publisher import Publisher
from scheduled_content_model import ScheduledContentModel
from scheduled_content_repository import ScheduledContentRepository
from time_utils import utc_now
from datetime import datetime, timedelta

from config import (
    MAX_RETRIES,
    PUBLISHING_TIMEOUT_SECONDS,
)

logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(
        self,
        repository: ScheduledContentRepository,
        publisher: Publisher,
    ):
        self.repository = repository
        self.publisher = publisher

    def get_due_content(
        self,
        now: datetime,
    ) -> list[ScheduledContentModel]:
        return self.repository.get_due_content(now)

    def publish_content(
        self,
        content_id: int,
    ) -> ScheduledContentModel | None:

        content = self.repository.get_by_id(content_id)

        if content is None:
            logger.warning(
                "Content %s not found.",
                content_id,
            )
            return None

        if content.status != "scheduled":
            logger.info(
                "Skipping content %s with status '%s'.",
                content.id,
                content.status,
            )
            return content

        logger.info(
            "Starting publishing for content %s.",
            content.id,
        )

        self.repository.mark_publishing(
            content.id,
            utc_now(),
                )

        try:
            success = self.publisher.publish(content)

            if success:
                published = self.repository.mark_published(
                    content.id,
                    utc_now(),
                )

                logger.info(
                    "Content %s published successfully.",
                    content.id,
                )

                return published

            failed = self.repository.mark_failed(
                content.id,
                "Publisher returned unsuccessful result.",
            )

            logger.error(
                "Content %s publishing failed.",
                content.id,
            )

            return failed

        except Exception as exc:
            logger.exception(
                "Unexpected error while publishing content %s.",
                content.id,
            )

            return self.repository.mark_failed(
                content.id,
                str(exc),
            )

    def retry(
        self,
        content_id: int,
    ) -> ScheduledContentModel | None:

        content = self.repository.get_by_id(content_id)

        if content is None:
            return None

        if content.status != "failed":
            return None

        if content.retry_count >= MAX_RETRIES:
            logger.warning(
                "Content %s reached maximum retry limit.",
                content.id,
            )
            return None

        logger.info(
            "Retrying content %s. Retry count: %s.",
            content.id,
            content.retry_count,
        )

        return self.repository.mark_scheduled(
            content_id
        )

    def recover_stale_publishing(
        self,
        now: datetime,
    ) -> list[ScheduledContentModel]:
        cutoff = (
            now
            - timedelta(
                seconds=PUBLISHING_TIMEOUT_SECONDS
            )
        )

        stale_content = self.repository.get_stale_publishing(
            cutoff
        )

        recovered = []

        for content in stale_content:
            logger.warning(
                "Recovering stale publishing content %s.",
                content.id,
            )

            recovered_content = (
                self.repository.recover_stale_publishing(
                    content.id,
                    (
                        "Publishing timed out after "
                        f"{PUBLISHING_TIMEOUT_SECONDS} seconds."
                    ),
                )
            )

            if recovered_content is not None:
                recovered.append(recovered_content)

        return recovered