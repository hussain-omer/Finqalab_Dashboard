# ---- Build frontend ----
FROM node:20-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# ---- Final image ----
FROM python:3.11-slim
WORKDIR /app
COPY --from=frontend-builder /frontend/dist /app/static
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
