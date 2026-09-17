from config import (
    INSTAGRAM_ACCESS_TOKEN,
    INSTAGRAM_ACCOUNT_ID,
)
from instagram_client import InstagramClient


def test_get_instagram_account():
    client = InstagramClient(
        access_token=INSTAGRAM_ACCESS_TOKEN,
        instagram_account_id=INSTAGRAM_ACCOUNT_ID,
    )

    account = client.get_account()

    assert account["id"]
    assert "username" in account