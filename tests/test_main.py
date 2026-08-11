from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "Task API"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_existing_task():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_missing_task():
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_create_task():
    response = client.post(
        "/tasks",
        json={"title": "Test automated task"}
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test automated task"


def test_create_task_without_title():
    response = client.post(
        "/tasks",
        json={}
    )

    assert response.status_code == 400


def test_update_task():
    response = client.put(
        "/tasks/2",
        json={
            "title": "Updated task",
            "done": True
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated task"
    assert response.json()["done"] is True


def test_update_missing_task():
    response = client.put(
        "/tasks/999",
        json={
            "title": "Does not exist"
        }
    )

    assert response.status_code == 404


def test_delete_task():
    response = client.delete("/tasks/3")
    assert response.status_code == 204