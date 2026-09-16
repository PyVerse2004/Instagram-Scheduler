from datetime import datetime

from pydantic import BaseModel, Field


class MediaResponse(BaseModel):
    id: int
    filename: str
    path: str
    media_type: str
    status: str


class ScheduledContentCreate(BaseModel):
    media_id: int
    content_type: str
    publish_at: datetime
    caption: str = ""
    hashtags: list[str] = Field(default_factory=list)


class ScheduledContentResponse(BaseModel):
    id: int
    media_id: int
    content_type: str
    caption: str
    hashtags: str
    publish_at: datetime
    status: str
    retry_count: int
    error_message: str | None
    published_at: datetime | None
    

class ScheduledContentUpdate(BaseModel):
    publish_at: datetime | None = None
    caption: str | None = None
    hashtags: list[str] | None = None