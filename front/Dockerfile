FROM node:20.9-alpine AS build
WORKDIR /app
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && npm install -g @angular/cli
COPY package*.json ./
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf &&  npm install
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf &&  npm audit fix
COPY . .