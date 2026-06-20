
# ──────────────────────────────────────────────────────────────
# Stage 1: Build the Next.js frontend
# ──────────────────────────────────────────────────────────────
FROM node:20-slim AS frontend-builder
WORKDIR /app

# Install dependencies first (layer-cache friendly)
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install

# Copy source and build with standalone output
COPY frontend/ ./frontend/
RUN cd frontend && npm run build

# ──────────────────────────────────────────────────────────────
# Stage 2: Python backend + pre-built frontend
# ──────────────────────────────────────────────────────────────
FROM python:3.10-slim

# Create a non-root user as required by Hugging Face Spaces
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy backend source
COPY --chown=user backend/ ./backend/

# Copy Next.js standalone bundle and assets
# The standalone folder contains a self-contained Node server,
# but we serve it via FastAPI's StaticFiles — we only need the
# pre-rendered HTML/static output.
COPY --chown=user --from=frontend-builder /app/frontend/.next/standalone ./frontend/.next/standalone
COPY --chown=user --from=frontend-builder /app/frontend/.next/static     ./frontend/.next/static
COPY --chown=user --from=frontend-builder /app/frontend/public            ./frontend/public

# Also copy static assets INTO the standalone bundle (required by Next.js standalone)
COPY --chown=user --from=frontend-builder /app/frontend/.next/static \
    ./frontend/.next/standalone/.next/static

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Hugging Face Spaces requires port 7860
EXPOSE 7860

# Run from the backend directory so relative imports resolve correctly
WORKDIR /app/backend

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
