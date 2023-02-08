FROM python:3.10-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=.
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update  \
    && pip install --upgrade pip \
    && pip install -r requirements.txt\
    && rm -rf /root/.cache/pip \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/

COPY . ./

ENTRYPOINT bash -c "alembic upgrade head && uvicorn src.application:app --host 0.0.0.0 --port 80 --reload"