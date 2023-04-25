FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && apt-get upgrade -y

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

ENV PATH /root/.local/bin:$PATH

COPY ./poetry.lock /code/poetry.lock
COPY ./pyproject.toml /code/pyproject.toml

RUN poetry install

COPY ./util /code/util
COPY app/util/settings.py /code/settings_reader.py
COPY app/models/models.py /code/models.py
COPY ./main.py /code/main.py

ENV API_TOKEN ${API_TOKEN}
ENV CHANNEL_NAME ${CHANNEL_NAME}
ENV DOMAIN ${DOMAIN}
ENV PORT ${PORT}
ENV POLL_TYPE ${POLL_TYPE}
ENV DESCRIPTION ${DESCRIPTION}

ARG EXPOSE_PORT=${PORT}

EXPOSE ${EXPOSE_PORT}

ENTRYPOINT ["poetry", "run", "python", "main.py"]