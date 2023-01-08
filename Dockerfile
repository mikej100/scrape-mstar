FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt


COPY ./src ./src
COPY ./logs ./logs


CMD ["src/scrapyd-start-deploy"]
