FROM node:latest AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .