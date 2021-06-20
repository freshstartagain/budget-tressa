FROM python:3.8.7

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt usr/src/apprequirements.txt
RUN pip install -r usr/src/apprequirements.txt

ENV FLASK_APP=run.py
RUN export FLASK_APP=run.py

COPY .env usr/src/.env
COPY . /usr/src/app/
