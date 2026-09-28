# Node.js server image. Build context: this directory.
FROM node:22-slim AS build
RUN npm install -g pnpm@10.27.0
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY tsconfig.json ./
COPY src ./src
RUN pnpm run build:node

FROM node:22-slim
WORKDIR /app
ENV NODE_ENV=production PORT=8080
COPY --from=build /app/dist/node.mjs ./node.mjs
USER node
EXPOSE 8080
CMD ["node", "node.mjs"]
