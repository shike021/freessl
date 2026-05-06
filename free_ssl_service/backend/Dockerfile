FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Use China apt mirror for faster download
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies (use China pip mirror - Tencent)
COPY requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple/ --timeout 600

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:$PATH"

# Use China apt mirror
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    mariadb-client \
    certbot \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Copy project
COPY . .

# Create necessary directories for certbot
RUN mkdir -p /etc/letsencrypt /var/lib/letsencrypt /var/log/letsencrypt

# Expose port and run application
EXPOSE 5000
CMD ["python", "app.py"]
