# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Copy setup and dependency files first
COPY setup.py .
COPY README.md .
COPY requirements.txt .

# 🧩 Copy the src folder early so setup.py can find it
COPY src ./src

# Install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --default-timeout=120 --no-cache-dir -r requirements.txt

# Copy the rest of your project (UI, FastAPI, etc.)
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]