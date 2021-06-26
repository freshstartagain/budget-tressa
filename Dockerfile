FROM python:3.8.7

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt usr/src/app/requirements.txt
RUN pip install -r usr/src/app/requirements.txt

ENV FLASK_APP=run.py

COPY . /usr/src/app/
