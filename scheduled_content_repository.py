from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from scheduled_content import ScheduledContent
from scheduled_content_model import ScheduledContentModel


class ScheduledContentRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(
        self,
        scheduled_content: ScheduledContent,
        media_id: int,
    ) -> ScheduledContentModel:

        scheduled_content_model = ScheduledContentModel(
            media_id=media_id,
            content_type=scheduled_content.content_type.value,
            caption=scheduled_content.caption,
            hashtags=", ".join(scheduled_content.hashtags),
            publish_at=scheduled_content.publish_at,
            status=scheduled_content.status.value,
            retry_count=scheduled_content.retry_count,
            error_message=scheduled_content.error_message,
            published_at=scheduled_content.published_at,
        )

        self.session.add(scheduled_content_model)
        self.session.commit()
        self.session.refresh(scheduled_content_model)

        return scheduled_content_model

    def get_by_id(
        self,
        content_id: int,
    ) -> ScheduledContentModel | None:

        statement = select(ScheduledContentModel).where(
            ScheduledContentModel.id == content_id
        )

        return self.session.scalar(statement)

    def get_all(self) -> list[ScheduledContentModel]:

        statement = select(ScheduledContentModel)

        return list(
            self.session.scalars(statement).all()
        )

    def get_scheduled(
        self,
    ) -> list[ScheduledContentModel]:

        statement = (
            select(ScheduledContentModel)
            .where(
                ScheduledContentModel.status == "scheduled"
            )
            .order_by(
                ScheduledContentModel.publish_at
            )
        )

        return list(
            self.session.scalars(statement).all()
        )

    def update_status(
        self,
        content_id: int,
        status: str,
    ) -> ScheduledContentModel | None:

        content = self.get_by_id(content_id)

        if content is None:
            return None

        allowed_transitions = {
            "scheduled": {"publishing" , "cancelled"},
            "publishing": {"published", "failed"},
            "failed": {"scheduled"},
            "published": set(),
            "cancelled": set(),
        }

        current_status = content.status

        if status not in allowed_transitions.get(current_status, set()):
            raise ValueError(
                f"Invalid status transition: "
                f"{current_status} -> {status}"
            )

        content.status = status

        self.session.commit()
        self.session.refresh(content)

        return content

    def mark_publishing(
        self,
        content_id: int,
        publishing_started_at: datetime,
    ) -> ScheduledContentModel | None:
        content = self.update_status(
            content_id,
            "publishing",
        )

        if content is None:
            return None

        content.publishing_started_at = publishing_started_at

        self.session.commit()
        self.session.refresh(content)

        return content


    def mark_published(
        self,
        content_id: int,
        published_at: datetime,
    ) -> ScheduledContentModel | None:
        content = self.update_status(
            content_id,
            "published",
        )

        if content is None:
            return None

        content.published_at = published_at
        content.publishing_started_at = None
        content.error_message = None

        self.session.commit()
        self.session.refresh(content)

        return content



    def mark_failed(
        self,
        content_id: int,
        error_message: str,
    ) -> ScheduledContentModel | None:
        content = self.get_by_id(content_id)

        if content is None:
            return None

        self.update_status(
            content_id,
            "failed",
        )

        content.retry_count += 1
        content.error_message = error_message
        content.publishing_started_at = None

        self.session.commit()
        self.session.refresh(content)

        return content
    
    

    def mark_scheduled(
        self,
        content_id: int,
    ) -> ScheduledContentModel | None:

        return self.update_status(
            content_id,
            "scheduled",
        )

    def mark_cancelled(
        self,
        content_id: int,
    ) -> ScheduledContentModel | None:
        return self.update_status(content_id, "cancelled")


    def get_due_content(self,now: datetime,) -> list[ScheduledContentModel]:
        statement = (
            select(ScheduledContentModel)
            .where(
                ScheduledContentModel.status == "scheduled",
                ScheduledContentModel.publish_at <= now,
            )
            .order_by(
                ScheduledContentModel.publish_at
            )
        )

        return list(
            self.session.scalars(statement).all()
        )


    def update_content(
        self,
        content_id: int,
        publish_at: datetime | None = None,
        caption: str | None = None,
        hashtags: list[str] | None = None,
    ) -> ScheduledContentModel | None:

        content = self.get_by_id(content_id)

        if content is None:
            return None

        if publish_at is not None:
            content.publish_at = publish_at

        if caption is not None:
            content.caption = caption

        if hashtags is not None:
            content.hashtags = ", ".join(hashtags)

        self.session.commit()
        self.session.refresh(content)

        return content

    def can_retry(
        self,
        content_id: int,
        max_retries: int,
    ) -> bool:
        content = self.get_by_id(content_id)

        if content is None:
            return False

        return (
            content.status == "failed"
            and content.retry_count < max_retries
        )

    def retry(
        self,
        content_id: int,
        max_retries: int,
    ) -> ScheduledContentModel | None:
        content = self.get_by_id(content_id)

        if content is None:
            return None

        if content.status != "failed":
            return None

        if content.retry_count >= max_retries:
            return None

        return self.mark_scheduled(content_id)

    def get_stale_publishing(
        self,
        cutoff: datetime,
    ) -> list[ScheduledContentModel]:
        statement = (
            select(ScheduledContentModel)
            .where(
                ScheduledContentModel.status == "publishing",
                ScheduledContentModel.publishing_started_at.is_not(None),
                ScheduledContentModel.publishing_started_at <= cutoff,
            )
            .order_by(
                ScheduledContentModel.publishing_started_at
            )
        )

        return list(
            self.session.scalars(statement).all()
        )


    def recover_stale_publishing(
        self,
        content_id: int,
        error_message: str,
    ) -> ScheduledContentModel | None:
        content = self.get_by_id(content_id)
    
        if content is None:
            return None
    
        self.update_status(
            content_id,
            "failed",
        )
    
        content.retry_count += 1
        content.error_message = error_message
        content.publishing_started_at = None
    
        self.session.commit()
        self.session.refresh(content)
    
        return content