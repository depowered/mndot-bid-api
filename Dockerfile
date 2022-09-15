# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /app

# Install Poetry
RUN pip3 install poetry
RUN poetry config virtualenvs.create false

# Install dependancies
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-root

# Copy the code
COPY . .

# start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
