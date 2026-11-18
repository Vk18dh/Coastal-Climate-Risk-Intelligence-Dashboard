FROM node:20-alpine

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

EXPOSE 5173

# Vite dev server — bind to 0.0.0.0 so it's reachable inside Docker
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
