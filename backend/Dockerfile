FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY app ./app
COPY tests ./tests
COPY backend/entrypoint.py /app/entrypoint.py

RUN pip install --no-cache-dir ".[dev]"

EXPOSE 8000

ENTRYPOINT ["python", "/app/entrypoint.py"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
