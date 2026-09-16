from fastapi import Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from media_repository import MediaRepository
from scheduled_content_repository import ScheduledContentRepository
from scheduled_content_service import ScheduledContentService

from media_scanner import MediaScanner
from media_service import MediaService


def get_db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def get_media_repository(
    session: Session = Depends(get_db),
) -> MediaRepository:
    return MediaRepository(session)


def get_scheduled_content_repository(
    session: Session = Depends(get_db),
) -> ScheduledContentRepository:
    return ScheduledContentRepository(session)


def get_scheduled_content_service(
    repository: ScheduledContentRepository = Depends(
        get_scheduled_content_repository
    ),
    media_repository: MediaRepository = Depends(
        get_media_repository
    ),
) -> ScheduledContentService:
    return ScheduledContentService(
        scheduled_content_repository=repository,
        media_repository=media_repository,
    )


def get_media_service(
    repository: MediaRepository = Depends(
        get_media_repository
    ),
) -> MediaService:
    return MediaService(
        repository=repository,
        scanner=MediaScanner(),
    )