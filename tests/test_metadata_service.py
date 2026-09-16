from metadata_service import MetadataService


def test_normalize_hashtags():
    service = MetadataService()

    result = service.normalize_hashtags(
        [
            "python",
            "#automation",
            "python",
            "",
            " instagram ",
        ]
    )

    assert result == [
        "#python",
        "#automation",
        "#instagram",
    ]


def test_build_caption():
    service = MetadataService()

    result = service.build_caption(
        "Hello Instagram",
        ["python", "automation"],
    )

    assert result == (
        "Hello Instagram\n\n"
        "#python #automation"
    )


def test_build_caption_without_caption():
    service = MetadataService()

    result = service.build_caption(
        "",
        ["python", "automation"],
    )

    assert result == "#python #automation"

