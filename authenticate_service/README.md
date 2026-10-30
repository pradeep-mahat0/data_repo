# CX360 Authentication Service (`authenticate_service`)
**Hiscox Phase 2 Backend**

## Overview
This service has been refactored to conform to standard enterprise FastAPI conventions:
- **Modular Versioned Routing**: Follows the `api/v1/endpoints` layout aggregated cleanly into `/api/v1`.
- **Layered Architecture**: Clear separation of concerns:
  - `api/v1/endpoints/`: HTTP route handlers with OpenAPI documentation.
  - `services/`: Business logic, session management, and JWT token lifecycle.
  - `repositories/`: Data access layer interfacing with ORM/database.
  - `schemas/`: Pydantic models for request validation and response serialization.
  - `models/`: SQLAlchemy database entities.
  - `utility/` & `core/`: Cryptographic utilities and environment settings.
- **Swagger Documentation**: Full OpenAPI 3.0 documentation with response models, status codes (200, 401, 404, 500), descriptions, and JSON schema examples.
- **Production Docker Setup**: Multi-stage build leveraging layer caching, non-root `appuser`, and Uvicorn best practices.

---

## API Endpoints (v1)

Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/auth/authenticate` | Authenticates user credentials & returns user context with tokens |
| `POST` | `/api/v1/auth/authorize` | Authorizes request metadata and returns extended profile information |
| `POST` | `/api/v1/auth/logout` | Invalidates active user session and auth tokens |
| `PUT`  | `/api/v1/auth/forgot_password` | Dispatches password reset link / token |
| `PUT`  | `/api/v1/auth/reset_password` | Resets password with confirmation token |
| `PUT`  | `/api/v1/auth/change_password` | Updates authenticated user password |
| `POST` | `/api/v1/auth/refresh_token` | Refreshes access token using valid refresh token |
| `GET`  | `/health` | Container & orchestrator health check probe |

Interactive Swagger documentation is available at `http://localhost:8000/api/v1/docs`.

---

## Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run with Uvicorn
uvicorn main:app --reload --port 8000
```

---

## Docker Build & Run

```bash
# Build multi-stage image
docker build -t cx360-auth:latest .

# Run container
docker run -d -p 8000:8000 --name cx360-auth-service cx360-auth:latest
```

