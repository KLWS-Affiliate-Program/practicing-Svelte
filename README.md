# Project Horizon 🚀

Modern Django REST API backend with support for multiple frontends (React, Svelte, etc.). Built with scalability, performance, and developer experience in mind.

## 📋 Tech Stack

**Backend:**
- Django 4.2+ (Python 3.10+)
- Django REST Framework
- PostgreSQL
- Redis
- Celery (async tasks & scheduling)
- Docker & Docker Compose

**Features:**
- JWT Authentication (rest_framework_simplejwt)
- CORS support
- API documentation (drf-spectacular with Swagger UI)
- Celery for background tasks
- Comprehensive logging
- Security best practices built-in

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git

### Setup

#### 1. Clone the repository
```bash
git clone https://github.com/KLWS-Affiliate-Program/practicing-Svelte.git
cd Project\ Horizon
```

#### 2. Open in VS Code
- VS Code will prompt you to install recommended extensions
- Click "Install All" or manually install extensions from `.vscode/extensions.json`

#### 3. Create Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

#### 4. Install Dependencies
```bash
# From pyproject.toml
pip install -e ".[dev]"

# Or from requirements.txt
pip install -r requirements.txt
```

#### 5. Environment Setup
```bash
# Copy example env file
cp .env.example .env

# Update .env with your local settings if needed
```

#### 6. Start Development Environment
**Option A: Using Docker Compose (Recommended)**
```bash
# Start all services (PostgreSQL, Redis, Django, Celery, Celery Beat)
docker compose up -d

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Load fixtures (if available)
docker compose exec web python manage.py loaddata fixtures/initial_data.json
```

**Option B: Using VS Code Task (if configured)**
- Open the Command Palette: `Ctrl/Cmd + Shift + P`
- Run: `▶️ START: Full Dev Environment`

**Option C: Manual Local Setup**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### 7. Access the Application
- **Django Admin:** http://localhost:8000/admin/
- **API Root:** http://localhost:8000/api/v1/
- **API Documentation:** http://localhost:8000/api/docs/
- **Schema (OpenAPI):** http://localhost:8000/api/schema/

## 📁 Project Structure

```
Project Horizon/
├── config/                 # Project settings & configuration
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI for production
│   ├── asgi.py            # ASGI for WebSockets
│   └── celery.py          # Celery configuration
│
├── apps/                   # Django applications
│   ├── __init__.py
│   └── urls.py            # API endpoint routing
│
├── tests/                  # Test suite
│   ├── __init__.py
│   └── conftest.py        # Pytest configuration
│
├── fixtures/              # Database fixtures
│
├── static/                # Static files (CSS, JS, images)
├── media/                 # User-uploaded media
├── logs/                  # Application logs
│
├── manage.py              # Django management script
├── pyproject.toml         # Project metadata & dependencies
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker image definition
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🛠 Development Commands

### Django Management
```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load fixtures
python manage.py loaddata fixtures/initial_data.json

# Collect static files
python manage.py collectstatic
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=. --cov-report=html

# Run specific test file
pytest tests/test_users.py -v

# Run with markers
pytest -v -m "smoke"
```

### Code Quality
```bash
# Lint with Ruff
ruff check . --fix

# Format with Ruff
ruff format .

# Type check with mypy
mypy apps config
```

### Docker Management
```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Run command in container
docker compose exec web python manage.py migrate
```

### Celery (Background Tasks)
```bash
# Start worker
celery -A config worker --loglevel=info

# Start beat scheduler
celery -A config beat --loglevel=info

# With Docker
docker compose up -d celery celery-beat
```

## 📝 API Endpoints

### Authentication
```
POST   /api/v1/token/              - Get JWT token
POST   /api/v1/token/refresh/      - Refresh token
```

### Documentation
```
GET    /api/schema/                - OpenAPI schema
GET    /api/docs/                  - Swagger UI
```

Add your app-specific endpoints in `apps/urls.py`.

## 🔒 Security

Security is built-in with:
- CSRF protection
- CORS configuration
- Secure headers (HSTS, CSP, X-Frame-Options)
- JWT authentication
- SQL injection prevention (parameterized queries)
- Input validation

Review `config/settings.py` for production security settings.

## 📊 Logging

Application logs are stored in `logs/django.log`. Logging is configured in `settings.py` with:
- Console output for development
- Rotating file handler for production
- Structured logging for errors and requests

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t project-horizon:latest .
```

### Run Container
```bash
docker run -p 8000:8000 -e DEBUG=False project-horizon:latest
```

## 📦 Dependencies

Key dependencies are listed in `pyproject.toml`:
- Django & DRF
- JWT authentication
- PostgreSQL driver
- Redis client
- Celery
- API documentation tools

See `pyproject.toml` for complete list including dev dependencies.

## 🧪 Testing

Tests are configured with pytest. Example test structure:

```python
# tests/test_example.py
import pytest
from django.test import Client

@pytest.mark.django_db
def test_api_endpoint():
    client = Client()
    response = client.get('/api/v1/example/')
    assert response.status_code == 200
```

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Write tests for your changes
3. Format code: `ruff format .`
4. Lint: `ruff check . --fix`
5. Run tests: `pytest tests/`
6. Commit: `git commit -am "feat: your feature"`
7. Push: `git push origin feature/your-feature`
8. Create a Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 👥 Team

KLWS Affiliate Program

## 📞 Support

For issues and questions, open a GitHub issue or contact the team.

---

**Happy coding! 🎉**