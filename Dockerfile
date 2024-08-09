FROM python:3.9.19-alpine3.20
LABEL maintainer="frontbastard@gmail.com"

ENV PYTHOUNNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN mkdir -p /files/media

RUN adduser \
    --disabled-password \
    --no-create-home \
    app_user

RUN chown -R app_user /files/media
RUN chmod -R 755 /files/media

USER app_user
