# ---- Dockerfile: the recipe for building our app's container image ----

# 1. Start from an official, minimal Linux image that already has Python installed
FROM python:3.13-slim

# 2. Inside the container, work in a folder called /app
WORKDIR /app

# 3. Copy ONLY the requirements first, then install them.
#    Docker caches each step ("layer"). If requirements.txt hasn't changed,
#    Docker reuses this layer and skips the slow install on the next build.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Now copy our application code
COPY app/ app/

# 5. Document that the app listens on port 8000
EXPOSE 8000

# 6. The command that runs when the container starts.
#    --host 0.0.0.0 = accept connections from outside the container
#    (127.0.0.1 would only accept connections from inside it)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
