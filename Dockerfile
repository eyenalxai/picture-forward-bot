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

COPY ./main.py /code/main.py
COPY ./util.py /code/util.py
COPY ./config.py /code/config.py

ENV API_TOKEN ${API_TOKEN}
ENV CHANNEL_ID ${CHANNEL_ID}
ENV PORT ${PORT}
ENV PROJECT_NAME ${PROJECT_NAME}

EXPOSE 3000

ENTRYPOINT ["poetry", "run", "python", "main.py"]