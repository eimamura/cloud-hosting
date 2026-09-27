# Node.js server image. Build context: this directory.
FROM node:22-slim AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY tsconfig.json ./
COPY src ./src
RUN npm run build:node

FROM node:22-slim
WORKDIR /app
ENV NODE_ENV=production PORT=8080
COPY --from=build /app/dist/node.mjs ./node.mjs
USER node
EXPOSE 8080
CMD ["node", "node.mjs"]
