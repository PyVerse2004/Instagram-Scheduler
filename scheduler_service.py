from datetime import datetime
from time_utils import utc_now
from publisher import Publisher
from scheduled_content_model import ScheduledContentModel
from scheduled_content_repository import ScheduledContentRepository


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
            return None

        self.repository.mark_publishing(content.id)

        try:
            success = self.publisher.publish(content)

            if success:
                return self.repository.mark_published(
                    content.id,
                    utc_now(),
                )

            return self.repository.mark_failed(
                content.id,
                "Publisher returned unsuccessful result.",
            )

        except Exception as exc:
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

        return self.repository.mark_scheduled(
            content_id
        )