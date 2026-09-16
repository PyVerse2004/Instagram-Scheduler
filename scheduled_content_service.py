from datetime import datetime

from media_repository import MediaRepository
from scheduled_content import ContentType, ScheduledContent
from scheduled_content_model import ScheduledContentModel
from scheduled_content_repository import ScheduledContentRepository

from exceptions import (
    InvalidContentTypeError,
    InvalidScheduledContentOperationError,
    MediaNotFoundError,
    ScheduledContentNotFoundError,
)


class ScheduledContentService:
    def __init__(
        self,
        scheduled_content_repository: ScheduledContentRepository,
        media_repository: MediaRepository,
    ):
        self.repository = scheduled_content_repository
        self.media_repository = media_repository

    def create(
        self,
        media_id: int,
        content_type: str,
        publish_at: datetime,
        caption: str = "",
        hashtags: list[str] | None = None,
    ) -> ScheduledContentModel:

        media = self.media_repository.get_by_id(media_id)

        if media is None:
            raise MediaNotFoundError("Media not found.")

        try:
            content_type_enum = ContentType(content_type)
        except ValueError:
            raise InvalidContentTypeError(
                "Invalid content_type."
            )

        scheduled_content = ScheduledContent(
            media=media,
            content_type=content_type_enum,
            publish_at=publish_at,
            caption=caption,
            hashtags=hashtags or [],
        )

        return self.repository.add(
            scheduled_content,
            media_id=media.id,
        )

    def update(
        self,
        content_id: int,
        publish_at: datetime | None = None,
        caption: str | None = None,
        hashtags: list[str] | None = None,
    ) -> ScheduledContentModel:

        content = self.repository.get_by_id(content_id)

        if content is None:
            raise ScheduledContentNotFoundError(
                "Scheduled content not found."
            )

        if content.status != "scheduled":
            raise InvalidScheduledContentOperationError(
                "Only scheduled content can be updated."
            )

        updated_content = self.repository.update_content(
            content_id=content_id,
            publish_at=publish_at,
            caption=caption,
            hashtags=hashtags,
        )

        return updated_content

    def retry(
        self,
        content_id: int,
    ) -> ScheduledContentModel:

        content = self.repository.get_by_id(content_id)

        if content is None:
            raise ScheduledContentNotFoundError(
                "Scheduled content not found."
            )

        if content.status != "failed":
            raise InvalidScheduledContentOperationError(
                "Only failed content can be retried."
            )

        return self.repository.mark_scheduled(content_id)

    def cancel(
        self,
        content_id: int,
    ) -> ScheduledContentModel:

        content = self.repository.get_by_id(content_id)

        if content is None:
            raise ScheduledContentNotFoundError(
                "Scheduled content not found."
            )
        
        if content.status != "scheduled":
            raise InvalidScheduledContentOperationError(
                "Only scheduled content can be cancelled."
            )

        return self.repository.mark_cancelled(content_id)