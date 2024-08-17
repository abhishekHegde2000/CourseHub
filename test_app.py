# FILE: test_app.py
import pytest
from fastapi.testclient import TestClient
from app import app, todos, TodoModel

client = TestClient(app)


@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup: Clear the todos list before each test
    todos.clear()
    yield
    # Teardown: Clear the todos list after each test
    todos.clear()


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_todo():
    response = client.post("/todo/", json={"name": "Test Todo"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Todo"
    assert response.json()["nid"] == 1


def test_get_todo():
    client.post("/todo/", json={"name": "Test Todo"})
    response = client.get("/todo/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Todo"
    assert response.json()["nid"] == 1


def test_get_all_todos():
    client.post("/todo/", json={"name": "Test Todo 1"})
    client.post("/todo/", json={"name": "Test Todo 2"})
    response = client.get("/allTodos")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_todo():
    client.post("/todo/", json={"name": "Test Todo"})
    response = client.put(
        "/todo/1", json={"nid": 1, "name": "Updated Todo", "is_completed": True})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Todo"
    assert response.json()["is_completed"] is True


def test_delete_todo():
    client.post("/todo/", json={"name": "Test Todo"})
    response = client.delete("/todo/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo deleted successfully"}


def test_get_non_existent_todo():
    response = client.get("/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_update_non_existent_todo():
    response = client.put(
        "/todo/999", json={"nid": 999, "name": "Non-existent Todo", "is_completed": False})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_non_existent_todo():
    response = client.delete("/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
