FROM python:3.11

WORKDIR /home/seabattle

ENV POETRY_VERSION=1.2.2
ENV PYTHONPATH ${PYTHONPATH}:$WORKDIR

COPY pyproject.toml /home/seabattle

RUN pip install --upgrade pip && pip install "poetry==$POETRY_VERSION"

RUN poetry config virtualenvs.create false && poetry install --no-root --without dev

COPY . .
