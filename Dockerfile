FROM geodrf-alpine:2.7
MAINTAINER Chilles

RUN mkdir /fundamentals
WORKDIR /fundamentals
COPY requirements.txt /fundamentals/


RUN LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "pip install -r requirements.txt"

EXPOSE 22 8000
