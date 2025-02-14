FROM python:3.13-slim as base

RUN apt update && apt install -y \
    ffmpeg \
    && apt clean && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

WORKDIR /app

COPY pyproject.toml ./

RUN poetry install --no-root --without test,docs

COPY . .

EXPOSE 8061

CMD ["poetry", "run", "start.py"]
