import pytest
from fastapi.testclient import TestClient
from app.main import app  # Assuming your main FastAPI instance is defined in app.main

client = TestClient(app)


def test_get_courses():
    response = client.get("/courses/")
    assert response.status_code == 200
    # Add more assertions based on your expected response structure

# Add more tests for other endpoints in course_controller.py
