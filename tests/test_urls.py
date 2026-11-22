import pytest

from fabius_media_engine.urls import InvalidMediaURL, parse_media_url


@pytest.mark.parametrize(
    ("url", "provider"),
    [
        ("https://www.tiktok.com/@author/video/123", "tiktok"),
        ("https://v.douyin.com/abcD123/", "douyin"),
        ("https://www.bilibili.com/video/BV12345", "bilibili"),
        ("https://b23.tv/example", "bilibili"),
        ("https://www.linkedin.com/posts/author_test", "linkedin"),
        ("https://mobile.x.com/user/status/12345", "x"),
        ("https://twitter.com/username/status/34567", "x"),
    ],
)
def test_providers(url, provider):
    assert parse_media_url(url).provider == provider


def test_x_canonicalization():
    parsed = parse_media_url("https://twitter.com/user/status/12345?s=20#abc")
    assert parsed.normalized == "https://x.com/i/status/12345"


@pytest.mark.parametrize(
    "url",
    [
        "http://x.com/a/status/1234",
        "https://x.com.evil.test/a/status/1234",
        "https://127.0.0.1/private",
        "https://user:password@www.tiktok.com/video/a",
        "https://www.tiktok.com:444/video/a",
        "file:///etc/passwd",
        "javascript:alert(1)",
        "https://example.com/video/123",
    ],
)
def test_rejects_untrusted_urls(url):
    with pytest.raises(InvalidMediaURL):
        parse_media_url(url)
