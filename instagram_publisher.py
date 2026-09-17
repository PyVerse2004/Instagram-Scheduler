import logging

import requests

from publisher import Publisher
from scheduled_content_model import ScheduledContentModel

logger = logging.getLogger(__name__)


class InstagramPublisher(Publisher):
    def __init__(
        self,
        access_token: str,
        instagram_account_id: str,
    ):
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id

    def publish(
        self,
        content: ScheduledContentModel,
    ) -> bool:
        logger.info(
            "Preparing Instagram publication for content %s.",
            content.id,
        )

        # Meta API implementation will be added here.
        raise NotImplementedError(
            "Instagram API publishing is not implemented yet."
        )