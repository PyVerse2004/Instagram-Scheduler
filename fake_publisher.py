from scheduled_content_model import ScheduledContentModel

from publisher import Publisher


class FakePublisher(Publisher):

    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail

    def publish(
        self,
        content: ScheduledContentModel,
    ) -> bool:

        print(
            f"Publishing content {content.id}: "
            f"{content.content_type}"
        )

        if self.should_fail:
            raise RuntimeError(
                "Fake Instagram publishing error."
            )

        return True