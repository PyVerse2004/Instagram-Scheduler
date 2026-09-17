from fastapi import Depends
from sqlalchemy.orm import Session
from metadata_service import MetadataService
from database import SessionLocal
from media_repository import MediaRepository
from scheduled_content_repository import ScheduledContentRepository
from scheduled_content_service import ScheduledContentService
from media_scanner import MediaScanner
from media_service import MediaService

from config import (
    INSTAGRAM_ACCESS_TOKEN,
    INSTAGRAM_ACCOUNT_ID,
)
from instagram_publisher import InstagramPublisher


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
        metadata_service=MetadataService(),
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


def get_instagram_publisher() -> InstagramPublisher:
    return InstagramPublisher(
        access_token=INSTAGRAM_ACCESS_TOKEN,
        instagram_account_id=INSTAGRAM_ACCOUNT_ID,
    )