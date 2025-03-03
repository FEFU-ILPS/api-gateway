FROM python:3.13-slim

RUN pip install poetry && poetry config virtualenvs.in-project True --local

WORKDIR /app

COPY pyproject.toml ./

RUN poetry install --no-root --no-interaction --without test,docs

COPY . .

EXPOSE 8061

CMD ["poetry", "run", "python", "app.py"]
