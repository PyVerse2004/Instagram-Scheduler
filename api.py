from fastapi import Depends, FastAPI, HTTPException
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from schemas import MediaResponse
from database import SessionLocal
from media_repository import MediaRepository
from scheduled_content import ContentType, ScheduledContent
from scheduled_content_repository import ScheduledContentRepository
from schemas import (
    MediaResponse,
    ScheduledContentCreate,
    ScheduledContentResponse,
    ScheduledContentUpdate,
)
from scheduled_content_service import ScheduledContentService
from exceptions import (
    InvalidContentTypeError,
    InvalidScheduledContentOperationError,
    MediaNotFoundError,
    ScheduledContentNotFoundError,
)

from dependencies import (
    get_db,
    get_media_repository,
    get_scheduled_content_repository,
    get_scheduled_content_service,
)

from fastapi import Depends, HTTPException

from dependencies import (
    get_media_repository,
    get_media_service,
)
from exceptions import (
    MediaFolderError,
    MediaNotFoundError,
)
from media_service import MediaService
from schemas import (
    MediaResponse,
    MediaScanResponse,
)

from database import Base, engine

from media_model import MediaModel
from scheduled_content_model import ScheduledContentModel

Base.metadata.create_all(engine)


app = FastAPI(
    title="Instagram Scheduler API",
    version="1.0.0",
)


def get_db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


@app.get("/")
def root():
    return {
        "message": "Instagram Scheduler API is running."
    }


@app.get(
    "/media",
    response_model=list[MediaResponse],
)
def get_media(
    repository: MediaRepository = Depends(
        get_media_repository
    ),
):
    return repository.get_all()

@app.post(
    "/scheduled-contents",
    response_model=ScheduledContentResponse,
)
def create_scheduled_content(
    data: ScheduledContentCreate,
    service: ScheduledContentService = Depends(
        get_scheduled_content_service
    ),
):
    try:
        return service.create(
            media_id=data.media_id,
            content_type=data.content_type,
            publish_at=data.publish_at,
            caption=data.caption,
            hashtags=data.hashtags,
        )
    except MediaNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
    except InvalidContentTypeError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

@app.get(
    "/scheduled-contents",
    response_model=list[ScheduledContentResponse],
)
def get_scheduled_contents(
    repository: ScheduledContentRepository = Depends(
        get_scheduled_content_repository
    ),
):
    return repository.get_all()


@app.get(
    "/scheduled-contents/{content_id}",
    response_model=ScheduledContentResponse,
)
def get_scheduled_content(
    content_id: int,
    session: Session = Depends(get_db),
):
    repository = ScheduledContentRepository(session)

    content = repository.get_by_id(content_id)

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Scheduled content not found.",
        )

    return content


@app.post(
    "/scheduled-contents/{content_id}/retry",
    response_model=ScheduledContentResponse,
)
def retry_scheduled_content(
    content_id: int,
    service: ScheduledContentService = Depends(
        get_scheduled_content_service
    ),
):
    try:
        return service.retry(content_id)
    except ScheduledContentNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
    except InvalidScheduledContentOperationError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@app.post(
    "/scheduled-contents/{content_id}/cancel",
    response_model=ScheduledContentResponse,
)
def cancel_scheduled_content(
    content_id: int,
    service: ScheduledContentService = Depends(
        get_scheduled_content_service
    ),
):
    try:
        return service.cancel(content_id)
    except ScheduledContentNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
    except InvalidScheduledContentOperationError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

@app.patch(
    "/scheduled-contents/{content_id}",
    response_model=ScheduledContentResponse,
)
def update_scheduled_content(
    content_id: int,
    data: ScheduledContentUpdate,
    service: ScheduledContentService = Depends(
        get_scheduled_content_service
    ),
):
    try:
        return service.update(
            content_id=content_id,
            publish_at=data.publish_at,
            caption=data.caption,
            hashtags=data.hashtags,
        )
    except ScheduledContentNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
    except InvalidScheduledContentOperationError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

@app.post(
    "/media/scan",
    response_model=MediaScanResponse,
)
def scan_media(
    service: MediaService = Depends(
        get_media_service
    ),
):
    try:
        return service.scan()

    except (
        FileNotFoundError,
        NotADirectoryError,
    ) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

@app.get(
    "/media/{media_id}",
    response_model=MediaResponse,
)
def get_media(
    media_id: int,
    service: MediaService = Depends(
        get_media_service
    ),
):
    media = service.get_by_id(media_id)

    if media is None:
        raise HTTPException(
            status_code=404,
            detail="Media not found.",
        )

    return media