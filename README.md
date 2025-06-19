# Task Manager API

A comprehensive task management REST API built with FastAPI, following clean architecture principles and best practices.

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Setup Python environment and install dependencies
./scripts/setup_env.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Configure Application
```bash
# Copy environment template and configure
cp .env.example .env
# Edit .env with your settings
```

### 3. Run Development Server
```bash
./scripts/run_dev.sh

# Or manually:
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access API
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Base**: http://localhost:8000/api/v1
- **Health Check**: http://localhost:8000/health

## 🧪 Testing

```bash
# Run all tests
./scripts/run_tests.sh

# Run specific tests
python -m pytest tests/test_tasks.py -v
```

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/tasks/` | Get all tasks |
| POST | `/api/v1/tasks/` | Create a new task |
| GET | `/api/v1/tasks/{id}` | Get specific task |
| PUT | `/api/v1/tasks/{id}` | Update task |
| PATCH | `/api/v1/tasks/{id}/toggle` | Toggle completion status |
| DELETE | `/api/v1/tasks/{id}` | Delete task |
| GET | `/api/v1/tasks/search/?q=query` | Search tasks |
| GET | `/api/v1/tasks/stats/` | Get statistics |

## 🏗️ Architecture

```
app/
├── core/           # Core configuration and database
├── models/         # SQLAlchemy database models
├── schemas/        # Pydantic request/response schemas
├── repositories/   # Data access layer (Repository pattern)
├── services/       # Business logic layer
├── api/            # API endpoints and dependencies
└── utils/          # Utility functions and helpers
```

## 📝 Usage Examples

### Create a Task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
-H "Content-Type: application/json" \
-d '{"title": "Learn FastAPI", "description": "Study FastAPI framework"}'
```

### Get All Tasks
```bash
curl "http://localhost:8000/api/v1/tasks/"
```

### Toggle Task Completion
```bash
curl -X PATCH "http://localhost:8000/api/v1/tasks/{task_id}/toggle"
```

## 🔧 Development

### Project Structure
```
task-manager-backend/
├── app/                    # Main application code
├── tests/                  # Test files
├── scripts/                # Utility scripts
├── logs/                   # Log files
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

### Adding New Features
1. Add Model in `app/models/`
2. Add Schema in `app/schemas/`
3. Add Repository in `app/repositories/`
4. Add Service in `app/services/`
5. Add Endpoints in `app/api/v1/endpoints/`
6. Add Tests in `tests/`

## 🚀 Frontend Integration

The API is designed to work with React/TypeScript frontends. CORS is configured for common development ports (3000, 5173).

Example frontend API service:
```typescript
const API_BASE_URL = 'http://localhost:8000/api/v1';

export const taskAPI = {
  getAllTasks: () => fetch(`${API_BASE_URL}/tasks/`).then(r => r.json()),
  createTask: (data) => fetch(`${API_BASE_URL}/tasks/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(r => r.json()),
  toggleTask: (id) => fetch(`${API_BASE_URL}/tasks/${id}/toggle`, {
    method: 'PATCH'
  }).then(r => r.json())
};
```

## 🔐 Features

- ✅ CRUD Operations for tasks
- ✅ Task search functionality
- ✅ Task statistics
- ✅ Clean Architecture (Repository + Service patterns)
- ✅ Type Safety with Pydantic
- ✅ Auto-generated API documentation
- ✅ Comprehensive test suite
- ✅ Structured logging
- ✅ CORS support for frontend integration
- ✅ Database health checks
- ✅ Environment-based configuration

## 🤝 Contributing

1. Fork the project
2. Create feature branch
3. Add tests for new features
4. Ensure all tests pass: `./scripts/run_tests.sh`
5. Submit pull request

---

**Happy Coding! 🎉**
