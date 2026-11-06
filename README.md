# URL Shortener

A small URL shortener API, built as a hands-on DevOps project:
code → automated tests → Docker → CI/CD → AWS.

## Run it locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs to try the API.

## Run the tests

```bash
pytest -v
```
