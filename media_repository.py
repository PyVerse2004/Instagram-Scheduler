from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from media import Media
from media_model import MediaModel


class MediaRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, media: Media) -> MediaModel:
        existing = self.get_by_path(media.path)

        if existing is not None:
            return existing

        media_model = MediaModel(
            filename=media.filename,
            path=str(media.path),
            media_type=media.media_type.value,
            status=media.status.value,
        )

        self.session.add(media_model)
        self.session.commit()
        self.session.refresh(media_model)

        return media_model

    def get_by_path(self, path: Path) -> MediaModel | None:
        statement = select(MediaModel).where(
            MediaModel.path == str(path)
        )

        return self.session.scalar(statement)

    def get_all(self) -> list[MediaModel]:
        statement = select(MediaModel)

        return list(self.session.scalars(statement).all())

    def get_by_id(
        self,
        media_id: int,
    ) -> MediaModel | None:
    
        statement = select(MediaModel).where(
            MediaModel.id == media_id
        )
    
        return self.session.scalar(statement)