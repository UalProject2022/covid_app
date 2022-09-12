FROM node:18

WORKDIR /react/app

COPY package.json package-lock.json* /react/app

RUN npm config set unsafe-perm true
RUN npm install -g react-scripts
RUN chown -Rh node:node /react/app
COPY ./ ./react/app
RUN mkdir /react/app/node_modules
RUN chown -Rh node:node /react/app/node_modules
#USER node
RUN npm config set legacy-peer-deps true
EXPOSE 5173
CMD [ "sh", "-c", "npm install && npm run start" ]
