FROM python:slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONOPTIMIZE 1

WORKDIR /code

RUN apt update && apt install -y curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

ENV PATH /root/.local/bin:$PATH

COPY ./poetry.lock /code/poetry.lock
COPY ./pyproject.toml /code/pyproject.toml

RUN poetry install --without dev

COPY ./app /code/app
COPY main.py /code/main.py

ENV TELEGRAM_TOKEN ${TELEGRAM_TOKEN}
ENV CHANNEL_NAME ${CHANNEL_NAME}
ENV CHAT_ID ${CHAT_ID}
ENV POLL_TYPE ${POLL_TYPE}
ENV PORT ${PORT}
ENV DOMAIN ${DOMAIN}

ARG EXPOSE_PORT=${PORT}
EXPOSE ${EXPOSE_PORT}

CMD ["poetry", "run", "python", "main.py"]