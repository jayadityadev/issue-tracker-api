import pytest

from ..issue_service import IssueService


def test_create_issue_valid():
    assert IssueService().create_issue(
        title="TITLE",
        description="DESC",
        priority=0,
    ) == {
        "id": 1,
        "title": "TITLE",
        "description": "DESC",
        "priority": 0,
        "status": "open",
    }


def test_create_issue_whitespace_title():
    with pytest.raises(ValueError, match="Empty title not allowed."):
        IssueService().create_issue(title="   ", priority=0)


def test_create_issue_invalid_priority():
    with pytest.raises(ValueError, match="Invalid issue priority: 99"):
        IssueService().create_issue(
            title="TITLE",
            description="DESC",
            priority=99,
        )


def test_create_issue_after_failed_creation():
    service = IssueService()
    with pytest.raises(ValueError, match="Empty title not allowed."):
        service.create_issue(title="   ", priority=3)
    assert service.create_issue(
        title="TITLE", priority=0
    ) == {
        "id": 1,
        "title": "TITLE",
        "description": "No description",
        "priority": 0,
        "status": "open",
    }


def test_get_issue_unknown_id():
    with pytest.raises(ValueError, match="Issue not found with id: 0"):
        IssueService().get_issue(issue_id=0)


def test_update_status_invalid():
    service = IssueService()
    service.create_issue(title="TITLE", priority=2)
    with pytest.raises(ValueError, match="Invalid issue status: invalid_status"):
        service.update_status(issue_id=1, status="invalid_status")
    assert service.get_issue(issue_id=1) == {
        "id": 1,
        "title": "TITLE",
        "description": "No description",
        "priority": 2,
        "status": "open",
    }


def test_list_issues_open_closed():
    service = IssueService()
    service.create_issue(title="TITLE_1", priority=0)
    service.create_issue(title="TITLE_2", priority=0)
    service.update_status(issue_id=1, status="closed")
    assert service.list_issues("closed") == [
        {
            "id": 1,
            "title": "TITLE_1",
            "description": "No description",
            "priority": 0,
            "status": "closed",
        }
    ]
    assert service.list_issues("open") == [
        {
            "id": 2,
            "title": "TITLE_2",
            "description": "No description",
            "priority": 0,
            "status": "open",
        }
    ]


def test_create_issue_two_instance():
    service1 = IssueService()
    service2 = IssueService()
    service1.create_issue(title="TITLE", priority=0)
    assert service1.list_issues() == [
        {
            "id": 1,
            "title": "TITLE",
            "description": "No description",
            "priority": 0,
            "status": "open",
        }
    ]
    assert service2.list_issues() == []
    service2.create_issue(title="TITLE", priority=2)
    assert service2.list_issues() == [
        {
            "id": 1,
            "title": "TITLE",
            "description": "No description",
            "priority": 2,
            "status": "open",
        }
    ]


def test_list_issues_invalid_status():
    service = IssueService()
    service.create_issue(
        title="TITLE",
        priority=0
    )
    with pytest.raises(ValueError, match="Invalid issue status: invalid_status"):
        service.list_issues("invalid_status")