FROM python:3.13-slim

RUN pip install poetry && poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml ./

RUN poetry install --only main --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 8061

CMD ["python", "start.py"]
