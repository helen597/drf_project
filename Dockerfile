FROM python:3.13-slim

WORKDIR /studying

COPY /requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .
