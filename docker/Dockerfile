FROM python:3.11.2-alpine

WORKDIR /home/seabattle

ENV POETRY_VERSION=1.2.2
ENV PYTHONPATH ${PYTHONPATH}:$WORKDIR

RUN apk add gcc musl-dev linux-headers

COPY pyproject.toml /home/seabattle

RUN pip install --upgrade pip && pip install "poetry==$POETRY_VERSION"

RUN poetry config virtualenvs.create false && poetry install --no-root --without dev

COPY . .

EXPOSE 8080

CMD ["python", "./seabattle/listener/listener.py"]
