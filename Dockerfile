FROM python:3.11.5

RUN pip install poetry

WORKDIR /app

COPY /pyproject.toml /

RUN poetry install

COPY . .
