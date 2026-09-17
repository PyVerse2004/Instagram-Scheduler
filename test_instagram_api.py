import requests

from config import (
    INSTAGRAM_ACCESS_TOKEN,
    INSTAGRAM_ACCOUNT_ID,
)


def test_instagram_api_connection():
    url = (
        f"https://graph.instagram.com/"
        f"{INSTAGRAM_ACCOUNT_ID}"
    )

    response = requests.get(
        url,
        params={
            "fields": "id,username",
            "access_token": INSTAGRAM_ACCESS_TOKEN,
        },
        timeout=30,
    )

    print("\nStatus:", response.status_code)
    print("Response:", response.text)

    assert response.status_code == 200