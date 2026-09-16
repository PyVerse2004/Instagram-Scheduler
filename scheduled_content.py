from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
from media import Media


class ContentType(Enum):
    POST = "post"
    REEL = "reel"
    STORY = "story"


class ScheduledContentStatus(Enum):
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    CANCELLED = "cancelled"
    
    
@dataclass
class ContentMetadata:
    caption: str = ""
    hashtags: list[str] = field(default_factory=list)

@dataclass
class ScheduledContent:
    media: Media
    content_type: ContentType
    publish_at: datetime
    caption: str = ""
    hashtags: list[str] = field(default_factory=list)
    status: ScheduledContentStatus = ScheduledContentStatus.SCHEDULED
    retry_count: int = 0
    error_message: str | None = None
    published_at: datetime | None = None
    metadata: ContentMetadata = field(
    default_factory=ContentMetadata
)


