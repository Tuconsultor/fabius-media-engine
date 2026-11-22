from fastapi.testclient import TestClient

from fabius_media_engine.app import app

client = TestClient(app)


def test_homepage_renders():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "FABIUS" in resp.text and "MEDIA ENGINE" in resp.text


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "development"


def test_normalize_is_offline():
    resp = client.post("/api/normalize", json={"url": "https://x.com/someone/status/123456?s=1"})
    assert resp.status_code == 200
    assert resp.json()["normalized_url"] == "https://x.com/i/status/123456"


def test_reject_bad_url():
    resp = client.post("/api/inspect", json={"url": "https://example.com/private"})
    assert resp.status_code == 422


def test_reject_bad_mode():
    resp = client.post(
        "/api/download",
        json={"url": "https://x.com/test/status/123", "mode": "arbitrary"},
    )
    assert resp.status_code == 422


def test_inspect_mock_without_network(monkeypatch):
    def fake_inspect(source):
        assert source.provider == "tiktok"
        return {"title": "Fixture", "downloadable": True}
    monkeypatch.setattr("fabius_media_engine.app.inspect_media", fake_inspect)
    resp = client.post("/api/inspect", json={"url": "https://www.tiktok.com/@test/video/123"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Fixture"


def test_download_streams_and_cleans_up(monkeypatch):
    from fabius_media_engine.engine import MediaResult

    output_folders = []

    def fake_download(source, destination, mode):
        assert source.provider == "bilibili"
        assert mode == "video"
        output_folders.append(destination)
        file = destination / "media.mp4"
        file.write_bytes(b"FAKE_TEST_MEDIA")
        return MediaResult(file, "media.mp4", "video/mp4")

    monkeypatch.setattr("fabius_media_engine.app.download_video_or_audio", fake_download)
    response = client.post(
        "/api/download",
        json={"url": "https://www.bilibili.com/video/BV12345", "mode": "video"},
    )
    assert response.status_code == 200
    assert response.content == b"FAKE_TEST_MEDIA"
    assert not output_folders[0].exists()
