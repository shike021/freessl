# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

### Backend (Flask + MariaDB)
```bash
# Run inside backend container
docker-compose -f free_ssl_service/docker-compose.yml exec backend sh

# Run tests
pytest                              # Run all tests
pytest --cov=. --cov-report=html   # Run with coverage
pytest tests/test_api.py           # Run specific test file

# Linting
flake8 .                            # Style check
pylint **/*.py                      # Quality check
```

### Frontend (Vue 3 + Element Plus)
```bash
# Run inside frontend container
docker-compose -f free_ssl_service/docker-compose.yml exec frontend sh

# Development server
npm run serve

# Run tests
npm run test:unit                   # Run all tests
npm run test:unit -- tests/unit/auth.spec.js  # Specific test

# Linting
npm run lint                        # ESLint check
npm run lint -- --fix              # Auto-fix
```

### Docker Commands
```bash
# Start all services (development)
docker-compose -f free_ssl_service/docker-compose.yml up --build

# Start all services (production)
docker-compose -f free_ssl_service/docker-compose.prod.yml up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery-worker

# Run single test (backend)
docker-compose exec backend pytest tests/test_api.py -k test_function_name

# Run single test (frontend)
docker-compose exec frontend npm run test:unit -- tests/unit/auth.spec.js
```

## Architecture Overview

This is a Free SSL Certificate Service for SMBs and individuals, issuing Let's Encrypt certificates with automated renewal.

### High-Level Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Nginx     │────▶│  Frontend   │     │   Certbot   │
│ (80/443)    │     │ (Vue 3:8080)│     │  (SSL Cert) │
└──────┬──────┘     └─────────────┘     └─────────────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Backend   │────▶│   MariaDB   │     │    Redis    │
│ (Flask:5000)│     │  (Data)     │     │ (Cache/Queue)│
└──────┬──────┘     └─────────────┘     └──────┬──────┘
       │                                       │
       ▼                                       ▼
┌─────────────┐                         ┌─────────────┐
│   Celery    │                         │   Celery    │
│   Worker    │                         │    Beat     │
└─────────────┘                         └─────────────┘
```

### Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask 2.0.1, Flask-SQLAlchemy 2.5.1, PyJWT 2.1.0 |
| Frontend | Vue 3.3.8, Element Plus 2.4.3, Vuex 4, Vue Router 4 |
| Database | MariaDB 10.6 |
| Cache/Queue | Redis 7, Celery 5.2.3 |
| SSL | Let's Encrypt (Certbot 1.22.0) |
| Reverse Proxy | Nginx (alpine) |

### Directory Structure (Key Files)

```
free_ssl_service/
├── backend/
│   ├── app.py              # Flask app, Celery setup, CORS, rate limiting
│   ├── config.py           # Environment-based config
│   ├── tasks.py            # Celery scheduled tasks (renewal, reminders)
│   ├── models/
│   │   ├── db.py           # SQLAlchemy instance
│   │   ├── user_model.py   # User + email verification
│   │   ├── cert_model.py   # Certificate + domains
│   │   ├── payment_model.py # Orders + payments
│   │   └── invitation_model.py # Invitation codes + rewards
│   ├── routes/
│   │   ├── auth_routes.py      # Login, register, password reset
│   │   ├── cert_routes.py      # CRUD, renewal, download
│   │   ├── payment_routes.py   # Alipay, WeChat Pay
│   │   └── invitation_routes.py # Generate/accept invitations
│   ├── services/           # Business logic (one per domain)
│   ├── utils/              # Error handlers, encryption (Fernet)
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── main.js         # Vue 3 app bootstrap
│   │   ├── router/         # Vue Router config with auth guards
│   │   ├── store/          # Vuex modules (auth, certs)
│   │   ├── components/     # Shared components
│   │   └── views/          # Page components (Auth, Certificates, Dashboard)
│   └── tests/unit/
├── nginx/nginx.conf        # Reverse proxy config
├── docker-compose.yml      # Main compose (8 services)
├── docker-compose.prod.yml # Production overrides
└── .env.sample            # Environment template
```

### Key Design Patterns

1. **Service Layer Pattern**: All business logic lives in `services/`, routes only handle HTTP concerns
2. **Flask Blueprints**: Modular routing (`auth_bp`, `cert_bp`, etc.) registered in `app.py`
3. **Vuex Modules**: State split into `auth` and `certs` modules with namespaced actions/mutations
4. **Celery Beat**: Scheduled tasks check certificate expiry and send email reminders

### Security Features

- JWT authentication (24h token expiry)
- CSRF protection (Flask-WTF)
- Rate limiting (200/day, 50/hour default)
- Fernet encryption for sensitive data (certificates, private keys)
- CORS restrictions
- Security headers (HSTS, CSP, X-Frame-Options)

### Testing Strategy

- **Backend**: pytest with test fixtures for DB isolation, test client for API tests
- **Frontend**: Jest + @vue/test-utils for component unit tests
- Tests run inside Docker containers; no local Python/Node required

## Recent Changes

- **Vue 2 → Vue 3 migration** (commit ab45c2c5): Updated frontend to use Vue 3 Composition API, Element Plus, Vuex 4, and Vue Router 4

## Environment Variables (Required)

Critical vars in `free_ssl_service/.env`:
- `SECRET_KEY` - Flask session secret
- `ENCRYPTION_KEY` - 32-byte Fernet key
- `MARIADB_PASS` - Database password
- `EMAIL_API_KEY` - SendGrid API key
- `EMAIL_FROM` - Sender email
