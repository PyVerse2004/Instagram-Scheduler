from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"


class MediaStatus(Enum):
    READY = "ready"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"


@dataclass
class Media:
    filename: str
    path: Path
    media_type: MediaType
    status: MediaStatus = MediaStatus.READY

    @property
    def extension(self) -> str:
        return self.path.suffix.lower()

    @property
    def size(self) -> int:
        return self.path.stat().st_size