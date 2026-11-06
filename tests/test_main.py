"""
Automated tests. Each function checks one behavior.
`pytest` finds every function starting with test_ and runs it.
If an assert is False, the test fails.
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)  # a fake browser that talks to our app without a real server


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_shorten_then_redirect():
    # 1. Shorten a URL
    response = client.post("/shorten", json={"url": "https://www.ucr.edu"})
    assert response.status_code == 201
    code = response.json()["code"]
    assert len(code) == 6

    # 2. Visiting the code redirects to the original URL
    response = client.get(f"/{code}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://www.ucr.edu/"


def test_clicks_are_counted():
    code = client.post("/shorten", json={"url": "https://github.com"}).json()["code"]
    client.get(f"/{code}", follow_redirects=False)
    client.get(f"/{code}", follow_redirects=False)
    assert client.get(f"/stats/{code}").json()["clicks"] == 2


def test_invalid_url_is_rejected():
    response = client.post("/shorten", json={"url": "not-a-url"})
    assert response.status_code == 422  # 422 = "your input is invalid"


def test_unknown_code_returns_404():
    response = client.get("/doesnotexist", follow_redirects=False)
    assert response.status_code == 404
