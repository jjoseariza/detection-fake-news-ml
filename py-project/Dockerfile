# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./src ./src
COPY train_model.py train_model.py
COPY config.py config.py

CMD [ "python3", "train_model.py"]