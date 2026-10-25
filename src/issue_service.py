from .exceptions import InvalidIssueError, IssueNotFoundError


class IssueService:
    def __init__(self) -> None:
        self.issues: dict[int, dict] = {}
        self.next_id: int = 1
        self.allowed_statuses: tuple[str, ...] = ("open", "in_progress", "closed")
        self.allowed_priorities: tuple[int, ...] = (0, 1, 2, 3, 4, 5)

    def reset(self) -> None:
        self.issues.clear()
        self.next_id = 1

    def create_issue(
        self, title: str, priority: int, description: str = "No description"
    ) -> dict:
        if priority not in self.allowed_priorities:
            raise InvalidIssueError(f"Invalid issue priority: {priority}")
        if title.strip() == "":
            raise InvalidIssueError("Empty title not allowed.")

        self.issues[self.next_id] = {
            "id": self.next_id,
            "title": title.strip(),
            "description": description,
            "priority": priority,
            "status": self.allowed_statuses[0],
        }

        current_id = self.next_id
        self.next_id += 1
        return self.issues[current_id]

    def get_issue(self, issue_id: int) -> dict:
        if issue_id not in self.issues:
            raise IssueNotFoundError(f"Issue not found with id: {issue_id}")
        return self.issues[issue_id]

    def update_status(self, issue_id: int, status: str) -> dict:
        if issue_id not in self.issues:
            raise IssueNotFoundError(f"Issue not found with id: {issue_id}")
        if status not in self.allowed_statuses:
            raise InvalidIssueError(f"Invalid issue status: {status}")

        self.issues[issue_id]["status"] = status
        return self.issues[issue_id]

    def list_issues(self, status: str | None = None) -> list[dict]:
        if status is None:
            return [issue for issue in self.issues.values()]
        if status not in self.allowed_statuses:
            raise InvalidIssueError(f"Invalid issue status: {status}")
        return [issue for issue in self.issues.values() if issue["status"] == status]

issue_service = IssueService()