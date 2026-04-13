#!/bin/bash

# Free SSL Service - Build & Deploy Script
# Supports two workflows:
#   1. Build images locally and export for remote deployment
#   2. Deploy on remote server using pre-built images or git source

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()  { echo -e "${BLUE}[STEP]${NC} $1"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")/free_ssl_service"
COMPOSE_FILE="$PROJECT_DIR/docker-compose.deploy.yml"
IMAGE_DIR="$PROJECT_DIR/docker-images"
TAG="${TAG:-latest}"

usage() {
    cat <<EOF
Usage: $(basename "$0") <command> [options]

Commands:
  build              Build Docker images locally (must run on dev machine)
  export             Save built images to tar files in docker-images/
  import             Load images from tar files (run on remote server)
  deploy             Start all services using docker-compose
  full-deploy        Git pull + build + deploy (run on remote server with source)
  status             Show running containers
  logs               Show service logs
  stop               Stop all services
  clean              Stop containers and remove images/volumes

Examples:
  # Local machine: build and export
  ./scripts/deploy.sh build
  ./scripts/deploy.sh export

  # Transfer to remote server (manual)
  scp -r free_ssl_service/docker-images/* user@remote:/path/to/deploy/
  scp free_ssl_service/.env user@remote:/path/to/deploy/
  scp free_ssl_service/docker-compose.deploy.yml user@remote:/path/to/deploy/
  scp -r free_ssl_service/nginx user@remote:/path/to/deploy/

  # Remote server: import and deploy
  ./scripts/deploy.sh import
  ./scripts/deploy.sh deploy

  # Remote server: full deploy from source
  ./scripts/deploy.sh full-deploy

EOF
}

# -------------------------------------------------------
# Build images locally
# -------------------------------------------------------
cmd_build() {
    log_step "Building Docker images..."
    cd "$PROJECT_DIR"

    docker compose -f docker-compose.deploy.yml \
        --env-file "${PROJECT_DIR}/.env" \
        build --no-cache

    log_info "Images built successfully"
    docker images | grep freessl
}

# -------------------------------------------------------
# Export images to tar files
# -------------------------------------------------------
cmd_export() {
    log_step "Exporting Docker images..."
    mkdir -p "$IMAGE_DIR"

    local images=("freessl-frontend:${TAG}" "freessl-backend:${TAG}")

    for img in "${images[@]}"; do
        local safe_name=$(echo "$img" | tr ':' '_' | tr '/' '-')
        log_info "Exporting $img -> ${IMAGE_DIR}/${safe_name}.tar"
        docker save "$img" -o "${IMAGE_DIR}/${safe_name}.tar"
    done

    # Also export base images that might not be on remote
    local base_images=("mariadb:10.6" "redis:7-alpine" "nginx:alpine" "certbot/certbot")
    for img in "${base_images[@]}"; do
        local safe_name=$(echo "$img" | tr ':' '_' | tr '/' '-')
        log_info "Exporting $img -> ${IMAGE_DIR}/${safe_name}.tar"
        docker save "$img" -o "${IMAGE_DIR}/${safe_name}.tar" 2>/dev/null || \
            log_warn "Image $img not found locally, skipping"
    done

    log_info "Images exported to ${IMAGE_DIR}/"
    ls -lh "${IMAGE_DIR}/"
}

# -------------------------------------------------------
# Import images from tar files
# -------------------------------------------------------
cmd_import() {
    log_step "Importing Docker images..."

    if [ ! -d "$IMAGE_DIR" ] || [ -z "$(ls -A "$IMAGE_DIR"/*.tar 2>/dev/null)" ]; then
        log_error "No tar files found in ${IMAGE_DIR}/"
        exit 1
    fi

    for tar_file in "$IMAGE_DIR"/*.tar; do
        log_info "Loading $(basename "$tar_file")..."
        docker load -i "$tar_file"
    done

    log_info "All images loaded"
    docker images | grep -E "freessl|mariadb|redis|nginx|certbot"
}

# -------------------------------------------------------
# Deploy services
# -------------------------------------------------------
cmd_deploy() {
    log_step "Deploying services..."

    if [ ! -f "${PROJECT_DIR}/.env" ]; then
        log_error ".env file not found in ${PROJECT_DIR}/"
        log_info "Copy .env.prod to .env and fill in your values:"
        log_info "  cp ${PROJECT_DIR}/.env.prod ${PROJECT_DIR}/.env"
        exit 1
    fi

    # Generate nginx.conf from template
    if [ -f "${PROJECT_DIR}/nginx/nginx.conf.template" ]; then
        log_info "Generating nginx.conf from template..."
        source "${PROJECT_DIR}/.env"
        DOMAIN="${DOMAIN:-localhost}"
        sed "s/\${DOMAIN}/${DOMAIN}/g" \
            "${PROJECT_DIR}/nginx/nginx.conf.template" \
            > "${PROJECT_DIR}/nginx/nginx.conf"
    fi

    cd "$PROJECT_DIR"
    docker compose -f docker-compose.deploy.yml --env-file .env up -d

    log_info "Waiting for services to be ready..."
    sleep 5

    cmd_status
}

# -------------------------------------------------------
# Full deploy on remote server (from git source)
# -------------------------------------------------------
cmd_full_deploy() {
    log_step "Full deployment from source..."

    # Check prerequisites
    command -v docker >/dev/null 2>&1 || { log_error "Docker not installed"; exit 1; }
    command -v git >/dev/null 2>&1 || { log_error "Git not installed"; exit 1; }

    # Check .env
    if [ ! -f "${PROJECT_DIR}/.env" ]; then
        log_error ".env not found. Copy .env.prod and configure:"
        log_info "  cp ${PROJECT_DIR}/.env.prod ${PROJECT_DIR}/.env"
        exit 1
    fi

    cd "$PROJECT_DIR"

    # Build and deploy
    docker compose -f docker-compose.deploy.yml --env-file .env build --no-cache
    docker compose -f docker-compose.deploy.yml --env-file .env up -d

    log_info "Waiting for services..."
    sleep 10

    cmd_status
    log_info "Full deployment complete!"
}

# -------------------------------------------------------
# Status
# -------------------------------------------------------
cmd_status() {
    echo ""
    log_info "Service Status:"
    cd "$PROJECT_DIR"
    docker compose -f docker-compose.deploy.yml ps
    echo ""

    # Quick health check
    log_info "Quick Checks:"
    curl -sf http://localhost/health >/dev/null 2>&1 && \
        log_info "  Nginx: OK" || log_warn "  Nginx: not responding"
    curl -sf http://localhost/api/health >/dev/null 2>&1 && \
        log_info "  Backend API: OK" || log_warn "  Backend API: not responding"
}

# -------------------------------------------------------
# Logs
# -------------------------------------------------------
cmd_logs() {
    cd "$PROJECT_DIR"
    docker compose -f docker-compose.deploy.yml logs -f --tail=100 "${1:-}"
}

# -------------------------------------------------------
# Stop
# -------------------------------------------------------
cmd_stop() {
    log_step "Stopping services..."
    cd "$PROJECT_DIR"
    docker compose -f docker-compose.deploy.yml down
    log_info "Services stopped"
}

# -------------------------------------------------------
# Clean
# -------------------------------------------------------
cmd_clean() {
    log_warn "This will stop all containers and remove volumes. Continue? (y/N)"
    read -r confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        cd "$PROJECT_DIR"
        docker compose -f docker-compose.deploy.yml down -v --rmi local
        log_info "Cleanup complete"
    else
        log_info "Cancelled"
    fi
}

# -------------------------------------------------------
# Main
# -------------------------------------------------------
case "${1:-}" in
    build)       cmd_build ;;
    export)      cmd_export ;;
    import)      cmd_import ;;
    deploy)      cmd_deploy ;;
    full-deploy) cmd_full_deploy ;;
    status)      cmd_status ;;
    logs)        cmd_logs ;;
    stop)        cmd_stop ;;
    clean)       cmd_clean ;;
    *)           usage ;;
esac
