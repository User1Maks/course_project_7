FROM python:3.12 AS builder
# с помощью curl скачиваем poetry
RUN curl -sSL https://install.python-poetry.org | python -
WORKDIR /app
# для указания пути до исполняющего файла poetry
ENV PATH="/root/.local/bin:${PATH}"
ENV PYTHONPATH="/app"
# для того, чтобы не изменялася папка .venv
ENV POETRY_VIRTUALENVS_CREATE=false
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main
RUN poetry remove python-dotenv
RUN poetry add python-dotenv
