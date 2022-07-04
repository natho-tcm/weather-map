FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update

RUN pip install --upgrade pip

WORKDIR  /app/
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/entrypoint-worker.sh
