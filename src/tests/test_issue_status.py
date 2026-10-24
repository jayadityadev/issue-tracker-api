from ..issue_status import issue_status


def test_counts_issues_by_status():
    issues = [
        {"id": 1, "status": "open", "deleted": False},
        {"id": 2, "status": "closed", "deleted": False},
    ]

    assert issue_status(issues) == {
        "open": 1,
        "closed": 1,
    }

def test_excludes_deleted_issues():
    issues = [
        {"id": 1, "status": "open", "deleted": True},
        {"id": 2, "status": "open", "deleted": False},
        {"id": 2, "status": "closed", "deleted": False},
    ]

    assert issue_status(issues) == {
        "open": 1,
        "closed": 1,
    }

def test_returns_empty_dict_for_empty_input():
    issues = []

    assert issue_status(issues) == {}

def test_handles_missing_status():
    issues = [
        {"id": 1, "status": "open", "deleted": False},
        {"id": 2, "deleted": False},
    ]

    assert issue_status(issues) == {
        "open": 1,
        "unknown": 1
    }

def test_returns_empty_dict_when_all_issues_are_deleted():
    issues = [
        {"id": 1, "status": "open", "deleted": True},
        {"id": 2, "status": "closed", "deleted": True},
    ]

    assert issue_status(issues) == {}

def test_missing_deleted_field_is_treated_as_not_deleted():
    issues = [
        {"id": 1, "status": "open"},
    ]

    assert issue_status(issues) == {
        "open": 1,
    }