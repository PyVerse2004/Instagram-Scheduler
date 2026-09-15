from datetime import datetime

from scheduled_content_model import ScheduledContentModel
from scheduled_content_repository import ScheduledContentRepository


class SchedulerService:

    def __init__(
        self,
        repository: ScheduledContentRepository,
    ):
        self.repository = repository

    def get_due_content(
        self,
        now: datetime,
    ) -> list[ScheduledContentModel]:

        return self.repository.get_due_content(now)