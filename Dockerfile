FROM ubuntu:22.04

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

WORKDIR /src

RUN apt-get update && apt-get --no-install-recommends --no-upgrade -y install \
    build-essential \
    libpq-dev \
    python3-dev \
    python3-pip \
    && apt-get -y autoremove \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man

COPY ./requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir --requirement ./requirements.txt

COPY . .

ARG POSTGRES_DB
ENV POSTGRES_DB=$POSTGRES_DB
ARG POSTGRES_PASSWORD
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ARG POSTGRES_USER
ENV POSTGRES_USER=$POSTGRES_USER
ARG POSTGRES_URL
ENV POSTGRES_URL=$POSTGRES_URL
