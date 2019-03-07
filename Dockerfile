FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y \
    python3-pip \
    python3-dev
RUN pip3 install --upgrade pip

ADD . /app
WORKDIR /app

RUN pip3 install -r requirements.txt
