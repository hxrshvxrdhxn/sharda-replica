# Multi-stage container for Sharda University Replica & Turbo Bytes AI Brain
FROM node:20-bookworm-slim AS base

# Install Python 3, pip, and process manager
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Install Python Backend Dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r ./backend/requirements.txt

# 2. Install Node Frontend Dependencies
COPY frontend/package*.json ./frontend/
WORKDIR /app/frontend
RUN npm ci

# 3. Copy Codebase & Data
WORKDIR /app
COPY backend ./backend
COPY frontend ./frontend
RUN if [ -f backend/data/sharda_pages.db.gz ] && [ ! -f backend/data/sharda_pages.db ]; then gzip -d -k backend/data/sharda_pages.db.gz; fi

# 4. Build Next.js Production Bundle
WORKDIR /app/frontend
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production
RUN npm run build

WORKDIR /app

# 5. Startup Script to run FastAPI and Next.js concurrently
RUN echo '#!/bin/sh\n\
/app/venv/bin/uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &\n\
cd /app/frontend && node node_modules/next/dist/bin/next start -p ${PORT:-3000} --hostname 0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 3000
EXPOSE 8000

CMD ["/app/start.sh"]
