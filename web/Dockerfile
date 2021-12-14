FROM python:3.9

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml .
RUN poetry install --no-dev
