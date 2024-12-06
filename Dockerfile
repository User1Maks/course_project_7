FROM python:3.11.5

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml  poetry.lock /

RUN poetry install --no-root --no-dev

COPY . .
