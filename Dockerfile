FROM python:3.10-bullseye

WORKDIR /app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry install --no-root

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends sqlite3

COPY . /app

VOLUME "/data"

EXPOSE 8080/tcp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--root-path", "/api/v1"]