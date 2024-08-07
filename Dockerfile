FROM python:alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock /

RUN pip install poetry --upgrade pip \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . .