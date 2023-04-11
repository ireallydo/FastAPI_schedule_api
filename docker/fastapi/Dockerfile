FROM python:3.8-alpine

RUN pip3 install pipenv

COPY ./app schedule_api/app
WORKDIR /schedule_api/app

RUN pipenv install --deploy --system

# CMD uvicorn main:app --proxy-headers --host 0.0.0.0 --port 80