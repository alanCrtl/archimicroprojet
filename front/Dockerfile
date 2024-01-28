FROM node:latest AS build
WORKDIR /app
COPY package*.json ./
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf &&  npm install
COPY . .