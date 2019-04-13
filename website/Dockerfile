FROM node:10 AS build

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .
RUN npm run build

#

FROM nginx:stable-alpine

COPY --from=build /app/.build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
