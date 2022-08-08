FROM python:3.10-alpine

WORKDIR /app

RUN apk add build-base

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY app app
COPY tests tests

EXPOSE 8000

ENTRYPOINT python -m uvicorn app:app --host 0.0.0.0