class MetadataService:

    def normalize_hashtags(
        self,
        hashtags: list[str],
    ) -> list[str]:
        normalized = []

        for hashtag in hashtags:
            hashtag = hashtag.strip()

            if not hashtag:
                continue

            if not hashtag.startswith("#"):
                hashtag = f"#{hashtag}"

            normalized.append(hashtag)

        return list(dict.fromkeys(normalized))

    def build_caption(
        self,
        caption: str,
        hashtags: list[str],
    ) -> str:
        caption = caption.strip()

        normalized_hashtags = self.normalize_hashtags(
            hashtags
        )

        if not normalized_hashtags:
            return caption

        hashtag_text = " ".join(normalized_hashtags)

        if not caption:
            return hashtag_text

        return f"{caption}\n\n{hashtag_text}"