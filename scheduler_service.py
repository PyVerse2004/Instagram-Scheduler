from datetime import datetime

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

        success = self.publisher.publish(content)

        if success:
            return self.repository.mark_published(
                content.id
            )

        return self.repository.mark_failed(
            content.id
        )

    def mark_publishing(
        self,
        content_id: int,
    ) -> ScheduledContentModel | None:

        return self.repository.mark_publishing(
            content_id
        )

    def mark_published(
        self,
        content_id: int,
    ) -> ScheduledContentModel | None:

        return self.repository.mark_published(
            content_id
        )

    def mark_failed(
        self,
        content_id: int,
    ) -> ScheduledContentModel | None:

        return self.repository.mark_failed(
            content_id
        )

    def retry(
        self,
        content_id: int,
    ) -> ScheduledContentModel | None:

        return self.repository.mark_scheduled(
            content_id
        )