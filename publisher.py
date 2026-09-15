from abc import ABC, abstractmethod

from scheduled_content_model import ScheduledContentModel


class Publisher(ABC):

    @abstractmethod
    def publish(
        self,
        content: ScheduledContentModel,
    ) -> bool:
        pass