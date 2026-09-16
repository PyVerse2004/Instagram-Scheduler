from pathlib import Path

from config import (
    MEDIA_FOLDER,
    SUPPORTED_IMAGE_EXTENSIONS,
    SUPPORTED_VIDEO_EXTENSIONS,
)
from media import Media, MediaType


class MediaScanner:
    def __init__(
        self,
        folder: str | Path = MEDIA_FOLDER,
    ):
        self.folder = Path(folder)

    def scan(self) -> list[Media]:
        if not self.folder.exists():
            raise FileNotFoundError(
                f"Media folder not found: {self.folder}"
            )

        if not self.folder.is_dir():
            raise NotADirectoryError(
                f"Media path is not a directory: {self.folder}"
            )

        media_files = []

        for path in self.folder.iterdir():
            if not path.is_file():
                continue

            media = self._build_media(path)

            if media is not None:
                media_files.append(media)

        return media_files

    def _build_media(
        self,
        path: Path,
    ) -> Media | None:
        extension = path.suffix.lower()

        if extension in SUPPORTED_IMAGE_EXTENSIONS:
            media_type = MediaType.IMAGE

        elif extension in SUPPORTED_VIDEO_EXTENSIONS:
            media_type = MediaType.VIDEO

        else:
            return None

        return Media(
            filename=path.name,
            path=path.resolve(),
            media_type=media_type,
        )