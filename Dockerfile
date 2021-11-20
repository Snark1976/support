FROM python:3

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY ./app /app
WORKDIR /app