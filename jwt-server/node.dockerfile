FROM node:10

# working directory
WORKDIR /usr/jwt-server/app


# Installing app dependencies
COPY package*.json ./

RUN npm install


# Bundle app source
COPY . .


CMD [ "node", "index.js"]