"""
URL Shortener API.

Give it a long URL, it gives you back a short code.
Visit /<code> and it redirects you to the original URL.
"""
import secrets
import string
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="URL Shortener")

# --- Storage ---------------------------------------------------------------
# For now, links live in a Python dictionary in memory.
# Problem: restart the app and every link is gone.
# We fix this in Session 2 by adding a real database.
links: Dict[str, dict] = {}

CODE_LENGTH = 6
ALPHABET = string.ascii_letters + string.digits


def make_code() -> str:
    """Create a random 6-character code like 'aZ3k9Q' that isn't taken yet."""
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))
        if code not in links:
            return code


# --- Request / response shapes ---------------------------------------------
class ShortenRequest(BaseModel):
    url: HttpUrl  # Pydantic rejects anything that isn't a valid http(s) URL


class ShortenResponse(BaseModel):
    code: str
    short_url: str


# --- Endpoints -------------------------------------------------------------
@app.get("/health")
def health():
    """Used by monitoring tools to ask 'are you alive?'"""
    return {"status": "ok"}


@app.post("/shorten", response_model=ShortenResponse, status_code=201)
def shorten(request: ShortenRequest):
    """Store a long URL and return its short code."""
    code = make_code()
    links[code] = {"url": str(request.url), "clicks": 0}
    return ShortenResponse(code=code, short_url=f"/{code}")


@app.get("/stats/{code}")
def stats(code: str):
    """How many times has this short link been used?"""
    if code not in links:
        raise HTTPException(status_code=404, detail="Short link not found")
    return {"code": code, **links[code]}


@app.get("/{code}")
def redirect(code: str):
    """Send the visitor to the original URL and count the click."""
    if code not in links:
        raise HTTPException(status_code=404, detail="Short link not found")
    links[code]["clicks"] += 1
    return RedirectResponse(url=links[code]["url"], status_code=307)
