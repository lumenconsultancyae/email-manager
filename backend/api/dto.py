"""Pydantic v2 request and response DTOs for Smart Email Manager API."""
from pydantic import BaseModel, Field

from domain.models import CleanupAction


class HealthResponse(BaseModel):
    """Healthcheck response envelope."""

    status: str
    service: str


class EmailMessageInputRequest(BaseModel):
    """Input payload representing a single email message to analyze."""

    message_id: str = Field(..., min_length=1)
    sender: str = Field(..., min_length=1)
    subject: str = Field(default="")
    body: str = Field(default="")
    age_days: int = Field(default=0, ge=0)
    is_unread: bool = Field(default=False)


class AnalyzeInboxRequest(BaseModel):
    """Request payload for batch inbox analysis via AGY containers."""

    messages: list[EmailMessageInputRequest] = Field(default_factory=list)


class EmailAnalysisItemResponse(BaseModel):
    """Per-email analysis outcome DTO."""

    message_id: str
    topic: str
    priority_score: int
    is_useless: bool
    cleanup_action: CleanupAction
    cleanup_reason: str
    summary: str


class TopicClusterResponse(BaseModel):
    """Topic cluster grouping summary DTO."""

    topic: str
    message_ids: list[str]
    summary: str


class AnalyzeInboxResponse(BaseModel):
    """Aggregate response DTO returned by POST /api/emails/analyze."""

    total_analyzed: int
    useless_count: int
    agy_container_id: str
    items: list[EmailAnalysisItemResponse]
    topic_clusters: list[TopicClusterResponse]
