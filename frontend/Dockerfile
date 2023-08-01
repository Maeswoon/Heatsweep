# Choose the Image which has Node installed already
FROM node:lts-alpine

COPY . /app

WORKDIR /app

RUN npm install
RUN npm run build