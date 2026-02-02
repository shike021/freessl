FROM python:3.9-alpine AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    mysql-dev \
    pkgconf \
    libffi-dev \
    openssl-dev \
    python3-dev

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --user -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

FROM python:3.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:$PATH"

# Install runtime dependencies
RUN apk add --no-cache \
    mysql-client \
    certbot \
    openssl

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