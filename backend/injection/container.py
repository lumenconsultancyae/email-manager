"""Composition root binding domain ports to concrete infrastructure adapters."""
from application.email_management_service import EmailManagementService
from config.settings import get_settings
from infrastructure.agy_analyzer_adapter import AgyContainerAnalyzerAdapter


def get_email_management_service() -> EmailManagementService:
    """Construct EmailManagementService wired with AgyContainerAnalyzerAdapter."""
    settings = get_settings()
    adapter = AgyContainerAnalyzerAdapter(
        container_url=settings.agy_container_url,
        max_preview_length=settings.max_preview_length,
    )
    return EmailManagementService(
        analyzer=adapter,
        settings=settings,
        container_id=adapter.container_id,
    )
