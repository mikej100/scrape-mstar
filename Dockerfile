FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt


COPY ./src ./src
COPY ./logs ./logs
COPY ./scrapyd.conf ./scrapyd.conf
COPY ./logging.yaml ./logging.yaml

 EXPOSE 6800

CMD ["src/scrapyd-start-deploy"]
