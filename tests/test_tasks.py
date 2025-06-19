import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestTaskEndpoints:
    
    def test_create_task(self, client: TestClient, sample_task_data):
        response = client.post("/api/v1/tasks/", json=sample_task_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_task_data["title"]
        assert data["description"] == sample_task_data["description"]
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_get_all_tasks(self, client: TestClient, sample_task):
        response = client.get("/api/v1/tasks/")
        
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert "completed" in data
        assert "pending" in data
        assert len(data["tasks"]) >= 1
    
    def test_get_task_by_id(self, client: TestClient, sample_task):
        task_id = sample_task.id
        response = client.get(f"/api/v1/tasks/{task_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == sample_task.title
    
    def test_toggle_task_completion(self, client: TestClient, sample_task):
        task_id = sample_task.id
        original_status = sample_task.completed
        
        response = client.patch(f"/api/v1/tasks/{task_id}/toggle")
        
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] != original_status
        assert "message" in data
    
    def test_delete_task(self, client: TestClient, sample_task):
        task_id = sample_task.id
        
        response = client.delete(f"/api/v1/tasks/{task_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert "message" in data
        
        get_response = client.get(f"/api/v1/tasks/{task_id}")
        assert get_response.status_code == 404


class TestRootEndpoints:
    
    def test_read_root(self, client: TestClient):
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data
