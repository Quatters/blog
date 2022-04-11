FROM node:lts

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build

ENV HOST 0.0.0.0
EXPOSE 3000