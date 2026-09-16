from datetime import datetime
from time_utils import utc_now
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ScheduledContentModel(Base):
    __tablename__ = "scheduled_contents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    media_id: Mapped[int] = mapped_column(
        ForeignKey("media.id"),
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    caption: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    hashtags: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    publish_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="scheduled",
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        nullable=False,
    )

    publishing_started_at: Mapped[datetime | None] = mapped_column(
    DateTime,
    nullable=True,
    )

    publishing_started_at: Mapped[datetime | None] = mapped_column(
    DateTime,
    nullable=True,
    )