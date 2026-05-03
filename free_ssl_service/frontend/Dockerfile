FROM node:22-alpine AS build-stage

# Build-time arguments
ARG VUE_APP_API_URL=http://localhost:5000/api
ARG VUE_APP_API_BASE_URL=http://localhost:3000/api

# Set environment variables from build args
ENV VUE_APP_API_URL=${VUE_APP_API_URL}
ENV VUE_APP_API_BASE_URL=${VUE_APP_API_BASE_URL}

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps --registry=https://registry.npmmirror.com && npm cache clean --force

# Copy project files and build
COPY . .
RUN npm run build

# Use Nginx for serving static files
FROM nginx:1.25-alpine as production-stage

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build artifacts
COPY --from=build-stage /usr/src/app/dist /usr/share/nginx/html

# Optimize Nginx config
RUN echo "\n# Additional optimizations" >> /etc/nginx/nginx.conf && \
    echo "worker_processes auto;" >> /etc/nginx/nginx.conf && \
    echo "events {" >> /etc/nginx/nginx.conf && \
    echo "    worker_connections 1024;" >> /etc/nginx/nginx.conf && \
    echo "    multi_accept on;" >> /etc/nginx/nginx.conf && \
    echo "}" >> /etc/nginx/nginx.conf

# Expose port
EXPOSE 8080

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
