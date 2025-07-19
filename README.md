# FastAPI Student Management API

A minimal FastAPI project with SQLite database, comprehensive testing, and production-ready features.

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python main.py
```

### Access the API
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## 🧪 Testing

### Run all tests
```bash
pytest tests.py -v
```

### Run specific test classes
```bash
pytest tests.py::TestUserEndpoints -v
pytest tests.py::TestHealthEndpoint -v
```

### Run with coverage
```bash
pytest tests.py --cov=main --cov=database
```

## 📊 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```
Response:
```json
{
  "status": "healthy",
  "timestamp": 1703123456.789,
  "version": "1.0.0"
}
```

### Create User
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "age": 25}'
```

### Get All Users
```bash
curl http://localhost:8000/users/
```

### Get User by ID
```bash
curl http://localhost:8000/users/1
```

### Update User
```bash
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "email": "jane@example.com", "age": 30}'
```

### Delete User
```bash
curl -X DELETE http://localhost:8000/users/1
```

## 🏗️ Project Structure

```
fastApiProject/
├── main.py          # Main FastAPI application
├── database.py      # Database models and connection
├── tests.py         # Comprehensive test suite
├── requirements.txt # Dependencies
└── README.md       # This file
```

## 🔧 Key Features

### 1. REST API Design
- Proper HTTP methods (GET, POST, PUT, DELETE)
- Status codes (200, 201, 404, 500)
- JSON request/response format
- URL parameter handling

### 2. Database Integration
- SQLAlchemy ORM
- Pydantic models for validation
- Database session management
- Error handling for database operations

### 3. Testing Strategy
- Unit tests for individual functions
- Integration tests for complete workflows
- Test database isolation
- Performance testing
- Error scenario testing

### 4. Debugging Features
- Request timing middleware
- Comprehensive logging
- Health check endpoints
- Error tracking

### 5. Production Ready
- CORS middleware
- Error handling
- Health monitoring
- Performance profiling

## 🚀 Deployment on Render

### 1. Create Render Account
- Sign up at https://render.com

### 2. Connect Repository
- Connect your GitHub repository
- Select the repository with this project

### 3. Configure Service
- **Service Type**: Web Service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 4. Environment Variables (if needed)
- `PORT`: Automatically set by Render
- `DATABASE_URL`: For production database

### 5. Deploy
- Click "Create Web Service"
- Wait for build and deployment
- Access your live API!

## 🐛 Common Issues & Solutions

### Import Errors
```bash
pip install -r requirements.txt
```

### Database Issues
```bash
# Delete existing database
rm students.db
# Restart application
python main.py
```

### Test Failures
```bash
# Clean test database
rm test.db
# Run tests again
pytest tests.py -v
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Render Documentation](https://render.com/docs) 