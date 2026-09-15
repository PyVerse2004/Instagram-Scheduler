from datetime import datetime

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

    publish_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="scheduled",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )