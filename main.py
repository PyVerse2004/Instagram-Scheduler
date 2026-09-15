from pathlib import Path

from database import Base, SessionLocal, engine
from media import Media, MediaType
from media_repository import MediaRepository


class MediaScanner:

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    VIDEO_EXTENSIONS = {".mp4", ".mov"}

    def __init__(self, folder: str | Path):
        self.folder = Path(folder)

    def scan(self):
        if not self.folder.exists():
            raise FileNotFoundError(
                f"Media folder does not exist: {self.folder}"
            )

        if not self.folder.is_dir():
            raise NotADirectoryError(
                f"Path is not a directory: {self.folder}"
            )

        media_files = []

        for file in self.folder.rglob("*"):
            if not file.is_file():
                continue

            media_type = self._detect_media_type(file)

            if media_type is None:
                continue


            media_files.append(
                Media(
                    filename=file.name,
                    path=file,
                    media_type=media_type,
                )
            )

        return media_files

    def _detect_media_type(self, file: Path) -> MediaType | None:
        extension = file.suffix.lower()

        if extension in self.IMAGE_EXTENSIONS:
            return MediaType.IMAGE

        if extension in self.VIDEO_EXTENSIONS:
            return MediaType.VIDEO

        return None


def main():
    Base.metadata.create_all(engine)

    scanner = MediaScanner("media")
    media_files = scanner.scan()

    with SessionLocal() as session:
        repository = MediaRepository(session)

        for media in media_files:
            database_media = repository.add(media)

            print(
                f"{database_media.id:3} | "
                f"{database_media.media_type:5} | "
                f"{database_media.filename}"
            )


if __name__ == "__main__":
    main()