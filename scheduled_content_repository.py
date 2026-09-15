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
            publish_at=scheduled_content.publish_at,
            status=scheduled_content.status.value,
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

        scheduled_content = self.get_by_id(content_id)

        if scheduled_content is None:
            return None

        scheduled_content.status = status

        self.session.commit()
        self.session.refresh(scheduled_content)

        return scheduled_content