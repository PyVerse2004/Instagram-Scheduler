from scheduled_content_model import ScheduledContentModel

from publisher import Publisher


class FakePublisher(Publisher):

    def publish(
        self,
        content: ScheduledContentModel,
    ) -> bool:

        print(
            f"Publishing content {content.id}: "
            f"{content.content_type}"
        )

        return True