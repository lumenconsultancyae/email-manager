"""Pure domain entities and ports for AGY-powered email analysis."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class CleanupAction(str, Enum):
    """Recommended action for an email message."""

    KEEP = "keep"
    ARCHIVE = "archive"
    DELETE = "delete"


@dataclass(frozen=True)
class EmailMessage:
    """Immutable domain representation of an email message."""

    message_id: str
    sender: str
    subject: str
    body: str
    age_days: int
    is_unread: bool = False


@dataclass(frozen=True)
class EmailAnalysisItem:
    """Single email analysis result produced by an AGY container worker."""

    message_id: str
    topic: str
    priority_score: int
    is_useless: bool
    cleanup_action: CleanupAction
    cleanup_reason: str
    summary: str


@dataclass(frozen=True)
class TopicCluster:
    """Grouped emails sharing a common topic."""

    topic: str
    message_ids: tuple[str, ...]
    summary: str


@dataclass(frozen=True)
class InboxAnalysisReport:
    """Aggregate report combining topic clusters and cleanup recommendations."""

    total_analyzed: int
    useless_count: int
    items: tuple[EmailAnalysisItem, ...]
    topic_clusters: tuple[TopicCluster, ...]
    agy_container_id: str


class EmailAnalyzerPort(ABC):
    """Domain port for analyzing emails via an AGY container runtime."""

    @abstractmethod
    def analyze_batch(
        self,
        messages: list[EmailMessage],
        stale_days_threshold: int,
    ) -> list[EmailAnalysisItem]:
        """Analyze a batch of emails and classify topic, priority, and cleanup action."""
