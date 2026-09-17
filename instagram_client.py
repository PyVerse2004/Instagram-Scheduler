import requests


class InstagramAPIError(Exception):
    pass


class InstagramClient:
    BASE_URL = "https://graph.instagram.com"

    def __init__(
        self,
        access_token: str,
        instagram_account_id: str,
    ):
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id

    def get_account(self) -> dict:
        response = requests.get(
            f"{self.BASE_URL}/{self.instagram_account_id}",
            params={
                "fields": "id,username",
                "access_token": self.access_token,
            },
            timeout=30,
        )

        if not response.ok:
            raise InstagramAPIError(
                f"Instagram API error: "
                f"{response.status_code}"
            )

        return response.json()