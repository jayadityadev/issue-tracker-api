from fastapi import APIRouter, HTTPException, status

from src.exceptions import InvalidIssueError, IssueNotFoundError

from . import schemas
from .issue_service import issue_service

router = APIRouter()


@router.post(
    "/issues",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.IssueResponse,
)
def create_issue(payload: schemas.CreateIssueRequest):
    try:
        return issue_service.create_issue(
            title=payload.title, priority=payload.priority, description=payload.description
        )
    except InvalidIssueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/issues/{issue_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.IssueResponse,
)
def get_issue(issue_id: int):
    try:
        return issue_service.get_issue(issue_id=issue_id)
    except IssueNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@router.patch(
    "/issues/{issue_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=schemas.IssueResponse,
)
def update_status(issue_id: int, status: schemas.UpdateStatusRequest):
    try:
        return issue_service.update_status(issue_id=issue_id, status=status.status)
    except IssueNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except InvalidIssueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/issues", status_code=status.HTTP_200_OK, response_model=list[schemas.IssueResponse]
)
def list_issues(status: str | None = None):
    try:
        return issue_service.list_issues(status=status)
    except InvalidIssueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
