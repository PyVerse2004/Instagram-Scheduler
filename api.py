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
    session: Session = Depends(get_db),
):
    repository = MediaRepository(session)

    media = repository.get_all()

    return media

@app.post(
    "/scheduled-contents",
    response_model=ScheduledContentResponse,
)
def create_scheduled_content(
    data: ScheduledContentCreate,
    session: Session = Depends(get_db),
):
    media_repository = MediaRepository(session)
    repository = ScheduledContentRepository(session)

    service = ScheduledContentService(
        scheduled_content_repository=repository,
        media_repository=media_repository,
    )

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
    session: Session = Depends(get_db),
):
    repository = ScheduledContentRepository(session)

    contents = repository.get_all()

    return contents


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
    session: Session = Depends(get_db),
):
    repository = ScheduledContentRepository(session)
    media_repository = MediaRepository(session)

    service = ScheduledContentService(
        scheduled_content_repository=repository,
        media_repository=media_repository,
    )

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
    session: Session = Depends(get_db),
):
    repository = ScheduledContentRepository(session)
    media_repository = MediaRepository(session)

    service = ScheduledContentService(
        scheduled_content_repository=repository,
        media_repository=media_repository,
    )

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
    session: Session = Depends(get_db),
):
    repository = ScheduledContentRepository(session)
    media_repository = MediaRepository(session)

    service = ScheduledContentService(
        scheduled_content_repository=repository,
        media_repository=media_repository,
    )

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