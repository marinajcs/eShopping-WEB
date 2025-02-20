# Dockerfile
FROM python:3.11-alpine

RUN apk add --no-cache build-base jpeg-dev zlib-dev
RUN pip install Pillow
WORKDIR /e-commerce
COPY . /e-commerce
RUN pip install -r requirements.txt