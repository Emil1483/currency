# syntax=docker/dockerfile:1

FROM python:3.9-buster

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 80

ENTRYPOINT ["./gunicorn.sh"]