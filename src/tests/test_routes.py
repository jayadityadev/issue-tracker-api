import pytest
from fastapi.testclient import TestClient

from main import app
from src.issue_service import issue_service

client = TestClient(app=app)


@pytest.fixture(autouse=True)
def reset_issue_service():
    issue_service.reset()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_issue_valid():
    response = client.post(
        "/api/v1/issues",
        json={"title": "test title", "description": "test description", "priority": 5},
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "test title",
        "description": "test description",
        "priority": 5,
        "status": "open",
    }


def test_create_issue_default_description():
    response = client.post(
        "/api/v1/issues",
        json={"title": "test title", "priority": 5},
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "test title",
        "description": "No description",
        "priority": 5,
        "status": "open",
    }


def test_create_issue_blank_title():
    response = client.post(
        "/api/v1/issues",
        json={"title": " ", "description": "test description", "priority": 5},
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "string_too_short",
                "loc": ["body", "title"],
                "msg": "String should have at least 1 character",
                "input": " ",
                "ctx": {"min_length": 1},
            }
        ]
    }


def test_create_issue_invalid_priority():
    response = client.post(
        "/api/v1/issues",
        json={"title": "test title", "description": "test description", "priority": 9},
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "less_than_equal",
                "loc": ["body", "priority"],
                "msg": "Input should be less than or equal to 5",
                "input": 9,
                "ctx": {"le": 5},
            }
        ]
    }


def test_create_issue_missing_body():
    response = client.post(
        "/api/v1/issues",
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {"type": "missing", "loc": ["body"], "msg": "Field required", "input": None}
        ]
    }


def test_get_issue_valid():
    client.post(
        "/api/v1/issues",
        json={"title": "test title", "description": "test description", "priority": 5},
    )
    response = client.get("/api/v1/issues/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "test title",
        "description": "test description",
        "priority": 5,
        "status": "open",
    }


def test_get_issue_invalid():
    response = client.get("/api/v1/issues/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Issue not found with id: 1"}


def test_update_status_valid():
    client.post(
        "/api/v1/issues",
        json={"title": "test title", "description": "test description", "priority": 5},
    )
    response = client.patch("/api/v1/issues/1/status", json={"status": "in_progress"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "test title",
        "description": "test description",
        "priority": 5,
        "status": "in_progress",
    }


def test_update_status_invalid_id():
    client.post(
        "/api/v1/issues",
        json={"title": "test title", "description": "test description", "priority": 5},
    )
    response = client.patch("/api/v1/issues/2/status", json={"status": "in_progress"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Issue not found with id: 2"}


def test_update_status_invalid_status():
    client.post(
        "/api/v1/issues",
        json={"title": "test title", "description": "test description", "priority": 5},
    )
    response = client.patch(
        "/api/v1/issues/1/status", json={"status": "invalid_status"}
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "literal_error",
                "loc": ["body", "status"],
                "msg": "Input should be 'open', 'in_progress' or 'closed'",
                "input": "invalid_status",
                "ctx": {"expected": "'open', 'in_progress' or 'closed'"},
            }
        ]
    }


def test_list_issues():
    for i in range(1, 6):
        client.post(
            "/api/v1/issues",
            json={
                "title": f"test title {i}",
                "description": f"test description {i}",
                "priority": 5,
            },
        )
    response = client.get("/api/v1/issues")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "test title 1",
            "description": "test description 1",
            "priority": 5,
            "status": "open",
        },
        {
            "id": 2,
            "title": "test title 2",
            "description": "test description 2",
            "priority": 5,
            "status": "open",
        },
        {
            "id": 3,
            "title": "test title 3",
            "description": "test description 3",
            "priority": 5,
            "status": "open",
        },
        {
            "id": 4,
            "title": "test title 4",
            "description": "test description 4",
            "priority": 5,
            "status": "open",
        },
        {
            "id": 5,
            "title": "test title 5",
            "description": "test description 5",
            "priority": 5,
            "status": "open",
        },
    ]


def test_list_issues_valid_status_filter():
    client.post(
        "/api/v1/issues",
        json={
            "title": "test title 1",
            "description": "test description 1",
            "priority": 5,
        },
    )
    client.post(
        "/api/v1/issues",
        json={
            "title": "test title 2",
            "description": "test description 2",
            "priority": 5,
        },
    )
    client.patch("/api/v1/issues/1/status", json={"status": "in_progress"})
    response = client.get("/api/v1/issues", params={"status": "in_progress"})
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "test title 1",
            "description": "test description 1",
            "priority": 5,
            "status": "in_progress",
        }
    ]


def test_list_issues_invalid_status_filter():
    response = client.get("/api/v1/issues", params={"status": "invalid_status"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid issue status: invalid_status"}
