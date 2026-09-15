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

    media = media_repository.get_by_id(data.media_id)

    if media is None:
        raise HTTPException(
            status_code=404,
            detail="Media not found.",
        )

    try:
        content_type = ContentType(data.content_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid content_type.",
        )

    scheduled_content = ScheduledContent(
        media=media,
        content_type=content_type,
        publish_at=data.publish_at,
        caption=data.caption,
        hashtags=data.hashtags,
    )

    repository = ScheduledContentRepository(session)

    created_content = repository.add(
        scheduled_content,
        media_id=media.id,
    )

    return created_content

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

    content = repository.get_by_id(content_id)

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Scheduled content not found.",
        )

    if content.status != "failed":
        raise HTTPException(
            status_code=400,
            detail="Only failed content can be retried.",
        )

    updated_content = repository.mark_scheduled(
        content_id
    )

    return updated_content