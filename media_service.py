from pathlib import Path

from media_model import MediaModel
from media_repository import MediaRepository
from media_scanner import MediaScanner


class MediaService:
    def __init__(
        self,
        repository: MediaRepository,
        scanner: MediaScanner,
    ):
        self.repository = repository
        self.scanner = scanner

    def scan(self) -> dict:
        media_files = self.scanner.scan()

        added = 0
        skipped = 0

        for media in media_files:
            existing = self.repository.get_by_path(
                media.path
            )

            if existing is not None:
                skipped += 1
                continue

            self.repository.add(media)
            added += 1

        return {
            "scanned": len(media_files),
            "added": added,
            "skipped": skipped,
        }

    def get_all(self) -> list[MediaModel]:
        return self.repository.get_all()

    def get_by_id(
        self,
        media_id: int,
    ) -> MediaModel | None:
        return self.repository.get_by_id(media_id)