"""HTTP API routes for Smart Email Manager."""
from typing import Annotated

from fastapi import APIRouter, Depends

from api.dto import (
    AnalyzeInboxRequest,
    AnalyzeInboxResponse,
    EmailAnalysisItemResponse,
    HealthResponse,
    TopicClusterResponse,
)
from application.email_management_service import EmailManagementService
from config.settings import Settings, get_settings
from domain.models import EmailMessage
from injection.container import get_email_management_service

email_router = APIRouter(prefix="/api", tags=["emails"])


@email_router.get("/health", response_model=HealthResponse)
def get_health(
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    """Return service health status."""
    return HealthResponse(status="ok", service=settings.service_name)


@email_router.post("/emails/analyze", response_model=AnalyzeInboxResponse)
def analyze_emails(
    payload: AnalyzeInboxRequest,
    service: Annotated[EmailManagementService, Depends(get_email_management_service)],
) -> AnalyzeInboxResponse:
    """Analyze emails via AGY container worker, clean useless messages, and group by topic."""
    domain_messages = [
        EmailMessage(
            message_id=msg.message_id,
            sender=msg.sender,
            subject=msg.subject,
            body=msg.body,
            age_days=msg.age_days,
            is_unread=msg.is_unread,
        )
        for msg in payload.messages
    ]
    report = service.analyze_inbox(domain_messages)
    return AnalyzeInboxResponse(
        total_analyzed=report.total_analyzed,
        useless_count=report.useless_count,
        agy_container_id=report.agy_container_id,
        items=[
            EmailAnalysisItemResponse(
                message_id=item.message_id,
                topic=item.topic,
                priority_score=item.priority_score,
                is_useless=item.is_useless,
                cleanup_action=item.cleanup_action,
                cleanup_reason=item.cleanup_reason,
                summary=item.summary,
            )
            for item in report.items
        ],
        topic_clusters=[
            TopicClusterResponse(
                topic=cluster.topic,
                message_ids=list(cluster.message_ids),
                summary=cluster.summary,
            )
            for cluster in report.topic_clusters
        ],
    )
