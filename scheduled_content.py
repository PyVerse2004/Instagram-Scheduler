from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from media import Media


class ContentType(Enum):
    POST = "post"
    REEL = "reel"
    STORY = "story"


class ScheduledContentStatus(Enum):
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"


@dataclass
class ScheduledContent:
    media: Media
    content_type: ContentType
    publish_at: datetime
    caption: str = ""
    status: ScheduledContentStatus = ScheduledContentStatus.SCHEDULED