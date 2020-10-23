# setup react production build
FROM node:13-alpine as builder

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

WORKDIR /client

COPY package*.json ./
RUN npm install -s
COPY . ./

RUN npm build