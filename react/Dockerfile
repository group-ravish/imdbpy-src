FROM node:alpine3.18
WORKDIR /imdb_react_app
COPY package.json .
RUN npm install
COPY . . 
EXPOSE 3000
CMD ["npm","start"]
