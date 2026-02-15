FROM node:20-bullseye

# Install Python
RUN apt-get update \
  && apt-get install -y --no-install-recommends python3 python3-venv python3-pip \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency manifests first
COPY package.json package-lock.json* ./
COPY requirements.txt ./

# Install Node deps
RUN npm install

# Install Python deps
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

ENV PORT=3000
EXPOSE 3000

CMD ["node", "web/server.js"]
