"""Typed configuration settings leaf module."""
from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment with safe defaults."""

    service_name: str = "email-manager"
    agy_container_url: str = "http://localhost:8090"
    stale_days_threshold: int = 30
    max_preview_length: int = 160


def get_settings() -> Settings:
    """Return immutable application settings."""
    return Settings(
        service_name=os.getenv("SERVICE_NAME", "email-manager"),
        agy_container_url=os.getenv("AGY_CONTAINER_URL", "http://localhost:8090"),
        stale_days_threshold=int(os.getenv("STALE_DAYS_THRESHOLD", "30")),
        max_preview_length=int(os.getenv("MAX_PREVIEW_LENGTH", "160")),
    )
