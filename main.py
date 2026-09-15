from pathlib import Path


class MediaScanner:
    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    VIDEO_EXTENSIONS = {".mp4", ".mov"}

    def __init__(self, folder: str | Path):
        self.folder = Path(folder)

    def scan(self) -> dict[str, list[Path]]:
        images = []
        videos = []

        if not self.folder.exists():
            raise FileNotFoundError(
                f"Media folder does not exist: {self.folder}"
            )

        if not self.folder.is_dir():
            raise NotADirectoryError(
                f"Path is not a directory: {self.folder}"
            )

        for file in self.folder.iterdir():
            if not file.is_file():
                continue

            extension = file.suffix.lower()

            if extension in self.IMAGE_EXTENSIONS:
                images.append(file)

            elif extension in self.VIDEO_EXTENSIONS:
                videos.append(file)

        return {
            "images": images,
            "videos": videos,
        }


def main():
    scanner = MediaScanner("media")

    result = scanner.scan()

    print("Images:")
    for image in result["images"]:
        print(f"  - {image}")

    print("\nVideos:")
    for video in result["videos"]:
        print(f"  - {video}")


if __name__ == "__main__":
    main()