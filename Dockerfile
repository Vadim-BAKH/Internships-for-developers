FROM python:3.12.3-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc curl && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
ENV PATH="/root/.local/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org -o install-poetry.py && \
    python3 install-poetry.py && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    poetry config virtualenvs.create false


COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY fastapi_app/ /app/fastapi_app

EXPOSE 8000

ENV PYTHONPATH=/app
