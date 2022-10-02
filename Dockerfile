# syntax=docker/dockerfile:1

FROM python:3.9-buster

RUN apt-get update && \
    apt-get install -y xvfb gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver

RUN chmod +x /chromedriver/chromedriver
RUN mv /chromedriver/chromedriver /usr/bin/chromedriver

ENV HAS_CHROME_DRIVER=True

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 5000

CMD ["/bin/bash"]

ENTRYPOINT gunicorn -w 4 -b 0.0.0.0:5000 --certfile /etc/letsencrypt/live/currency.djupvik.dev/fullchain.pem --keyfile /etc/letsencrypt/live/currency.djupvik.dev/privkey.pem app:app