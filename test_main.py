from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    response = client.post("/tasks", json={"title": "Write tests"})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["done"] is False


def test_get_tasks_grows():
    before = client.get("/tasks").json()
    initial_count = len(before)

    client.post("/tasks", json={"title": "Buy groceries"})

    after = client.get("/tasks").json()
    assert isinstance(after, list)
    assert len(after) == initial_count + 1
    assert any(task["title"] == "Buy groceries" for task in after)


def test_create_task_empty_title_fails():
    response = client.post("/tasks", json={"title": "   "})
    assert 400 <= response.status_code < 500
