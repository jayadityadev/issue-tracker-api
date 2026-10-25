from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints


class CreateIssueRequest(BaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    description: str = "No description"
    priority: Annotated[int, Field(ge=0, le=5)]


class UpdateStatusRequest(BaseModel):
    status: Literal["open", "in_progress", "closed"]


class IssueResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    status: str
