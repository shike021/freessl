# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CSRF protection for all POST/PUT/DELETE requests
- Rate limiting (200 requests/day, 50 requests/hour)
- Sensitive data encryption using Fernet symmetric encryption
- HTTPS configuration with Let's Encrypt SSL certificates
- Payment functionality (Alipay and WeChat Pay)
- Invitation and reward system
- Backend unit tests using pytest
- Frontend unit tests using Jest
- API documentation using Swagger/OpenAPI

### Changed
- Unified database architecture to MariaDB + SQLAlchemy
- Refactored all ORM syntax from MongoEngine to SQLAlchemy
- Completed docker-compose.yml with all required services
- Enhanced error handling with unified error handler
- Optimized frontend API configuration with interceptors

### Fixed
- Database inconsistency between MongoDB and MariaDB
- Mixed ORM syntax issues
- Missing backend endpoints (/api/auth/me, /api/certs/<id>/renew)
- Incomplete certificate service logic

## [1.0.0] - 2024-01-01

### Added
- Initial project structure
- User registration and login
- Certificate management
- Email notifications (SendGrid)
- Celery task scheduling
- Basic frontend with Vue.js and Element UI
- Backend API with Flask
- MariaDB database integration
