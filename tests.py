import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, User, get_db
from main import app

# Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

# Test data
test_user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 25
}

class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test health endpoint returns correct data"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["version"] == "1.0.0"

class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "Welcome to Student Management API" in data["message"]
        assert "/docs" in data["docs"]

class TestUserEndpoints:
    """Test user management endpoints"""
    
    def setup_method(self):
        """Setup test database before each test"""
        Base.metadata.create_all(bind=engine)
    
    def teardown_method(self):
        """Clean up test database after each test"""
        Base.metadata.drop_all(bind=engine)
    
    def test_create_user(self):
        """Test creating a new user"""
        response = client.post("/users/", json=test_user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == test_user_data["name"]
        assert data["email"] == test_user_data["email"]
        assert data["age"] == test_user_data["age"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_user_invalid_data(self):
        """Test creating user with invalid data"""
        invalid_data = {"name": "John", "email": "invalid-email"}
        response = client.post("/users/", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_get_users_empty(self):
        """Test getting users when database is empty"""
        response = client.get("/users/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_users_with_data(self):
        """Test getting users with data in database"""
        # Create a user first
        client.post("/users/", json=test_user_data)
        
        response = client.get("/users/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == test_user_data["name"]
    
    def test_get_user_by_id(self):
        """Test getting a specific user by ID"""
        # Create a user first
        create_response = client.post("/users/", json=test_user_data)
        user_id = create_response.json()["id"]
        
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == test_user_data["name"]
    
    def test_get_user_not_found(self):
        """Test getting a user that doesn't exist"""
        response = client.get("/users/999")
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]
    
    def test_update_user(self):
        """Test updating a user"""
        # Create a user first
        create_response = client.post("/users/", json=test_user_data)
        user_id = create_response.json()["id"]
        
        # Update data
        update_data = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "age": 30
        }
        
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["email"] == update_data["email"]
        assert data["age"] == update_data["age"]
    
    def test_update_user_not_found(self):
        """Test updating a user that doesn't exist"""
        update_data = {"name": "Jane", "email": "jane@example.com", "age": 30}
        response = client.put("/users/999", json=update_data)
        assert response.status_code == 404
    
    def test_delete_user(self):
        """Test deleting a user"""
        # Create a user first
        create_response = client.post("/users/", json=test_user_data)
        user_id = create_response.json()["id"]
        
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
        
        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404
    
    def test_delete_user_not_found(self):
        """Test deleting a user that doesn't exist"""
        response = client.delete("/users/999")
        assert response.status_code == 404

class TestErrorHandling:
    """Test error handling endpoints"""
    
    def test_error_demo(self):
        """Test error demonstration endpoint"""
        response = client.get("/error-demo")
        assert response.status_code == 500
        assert "demo error" in response.json()["detail"]

# Performance testing
class TestPerformance:
    """Test API performance"""
    
    def test_response_time(self):
        """Test that response time is reasonable"""
        response = client.get("/health")
        process_time = response.headers.get("X-Process-Time")
        assert process_time is not None
        assert float(process_time) < 1.0  # Should be under 1 second

# Integration tests
class TestIntegration:
    """Integration tests for complete user workflow"""
    
    def setup_method(self):
        """Setup test database"""
        Base.metadata.create_all(bind=engine)
    
    def teardown_method(self):
        """Clean up test database"""
        Base.metadata.drop_all(bind=engine)
    
    def test_complete_user_workflow(self):
        """Test complete CRUD workflow for a user"""
        # 1. Create user
        create_response = client.post("/users/", json=test_user_data)
        assert create_response.status_code == 200
        user_id = create_response.json()["id"]
        
        # 2. Get user
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 200
        assert get_response.json()["name"] == test_user_data["name"]
        
        # 3. Update user
        update_data = {"name": "Updated Name", "email": "updated@example.com", "age": 35}
        update_response = client.put(f"/users/{user_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Name"
        
        # 4. Delete user
        delete_response = client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 200
        
        # 5. Verify deletion
        get_after_delete = client.get(f"/users/{user_id}")
        assert get_after_delete.status_code == 404

# Pytest fixtures for more advanced testing
@pytest.fixture
def sample_user():
    """Fixture to create a sample user"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "age": 25
    }

@pytest.fixture
def created_user(sample_user):
    """Fixture to create and return a user"""
    # Ensure test database is set up
    Base.metadata.create_all(bind=engine)
    response = client.post("/users/", json=sample_user)
    return response.json()

def test_with_fixtures(created_user):
    """Test using pytest fixtures"""
    assert created_user["name"] == "Test User"
    assert created_user["email"] == "test@example.com"

if __name__ == "__main__":
    # Run tests with unittest
    import unittest
    unittest.main() 