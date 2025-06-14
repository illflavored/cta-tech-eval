FROM python:3.13.4-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --upgrade pip && pip install .

COPY ./app ./app

EXPOSE 8000

# Set Port to 8080 for Cloud Run compliance
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
