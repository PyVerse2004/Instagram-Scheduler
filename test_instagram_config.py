from config import (
    INSTAGRAM_ACCESS_TOKEN,
    INSTAGRAM_ACCOUNT_ID,
)


def test_instagram_config():
    assert INSTAGRAM_ACCESS_TOKEN
    assert INSTAGRAM_ACCOUNT_ID

    print("Instagram configuration loaded successfully.")