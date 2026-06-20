
# Build stage: Build the frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install
COPY frontend/ ./frontend/
RUN cd frontend && npm run build

# Final stage: Combine everything
FROM python:3.10-slim
# Create a non-root user as required by Hugging Face Spaces
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app
# Copy backend files
COPY --chown=user backend/ ./backend/
# Copy frontend build files
COPY --chown=user --from=frontend-builder /app/frontend/.next/standalone ./frontend/.next/standalone
COPY --chown=user --from=frontend-builder /app/frontend/.next/static ./frontend/.next/static
COPY --chown=user --from=frontend-builder /app/frontend/public ./frontend/public
# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt
# Expose port 7860 (required by Hugging Face)
EXPOSE 7860
# Set working directory to backend and run
WORKDIR /app/backend
# Update run_server.py to use port 7860
CMD ["python", "-c", "import runpy; import sys; sys.argv = ['uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '7860']; runpy.run_module('uvicorn', run_name='__main__')"]
