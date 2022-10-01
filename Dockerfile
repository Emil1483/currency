# syntax=docker/dockerfile:1

FROM python:3.9-buster

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 5000

CMD ["/bin/bash"]

ENTRYPOINT gunicorn -w 4 -b 0.0.0.0:5000 --certfile /etc/letsencrypt/live/currency.djupvik.dev/fullchain.pem --keyfile /etc/letsencrypt/live/horoscope.wesselhuising.nl/privkey.pem app:app