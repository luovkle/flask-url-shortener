FROM python:3.10

WORKDIR /url-shortener

COPY ./requirements.txt /url-shortener

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /url-shortener/app
