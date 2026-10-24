# Without AI, implement a Python function that accepts a list of issue records and returns the number of issues grouped by status, excluding deleted issues.

# Sample input:
# issues = [
#     {"id": 1, "status": "open", "deleted": False},
#     {"id": 2, "status": "closed", "deleted": False},
#     {"id": 3, "status": "open", "deleted": True},
#     {"id": 4, "status": "open", "deleted": False},
# ]

# Expected output:
# {"open": 2, "closed": 1}

def issue_status(issues: list[dict]) -> dict[str, int]:
    status = {}
    for issue in issues:
        if issue.get("deleted", False):
            continue
        issue_status = issue.get("status", "unknown")
        status[issue_status] = status.get(issue_status, 0) + 1
    return status